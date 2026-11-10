# Plan-to-Tutor API server (Ansible)

This playbook sets up the Plan-to-Tutor backend API on Ubuntu 24.04.
One server can run more than one instance of the API.

- One systemd unit per instance serves the API and runs the background jobs from the MySQL `jobs` table.
- nginx is the only public listener, and it serves nothing but `/api/`.
- Each deploy pulls the code from git, applies the migrations, and restarts the API when the code changed.
- A systemd timer dumps the database of each instance every night, optionally to a private GitHub repository too.
- certbot gets the TLS certificate and renews it.
- The frontend is a static Vite build on Cloudflare Pages, not on this server.

| Component | What | Listens on |
| --- | --- | --- |
| MySQL | MySQL 9.7 LTS from the MySQL APT repository, collation `utf8mb4_0900_as_cs`. All instances share it. | localhost:3306 |
| `api_service` | FastAPI under uvicorn, with the job runner | 127.0.0.1:`backend_port` |
| nginx | `/api/` proxy, with the `/api` prefix removed. All instances share it. | 0.0.0.0:`api_public_port` |
| `db_backup_unit`.timer | Nightly `mysqldump` of the instance database | none |

## Instances

The shared host `greencloud` (its address is `ansible_host` in `inventory.ini`) runs two instances.
Each instance is a host in the inventory, and both hosts point at the same server.

| Name | Production (`greencloud`) | Staging (`greencloud-staging`) |
| --- | --- | --- |
| Code | a release tag, `-e release_tag=vYYYY.MM.DD` | `main` |
| `app_root` | `/opt/lpcg` | `/opt/lpcg-staging` |
| `api_service` | `ptt-api` | `ptt-api-staging` |
| `backend_port` | 8010 | 8011 |
| `db_name`, `db_user` | `lpcg` | `lpcg_staging` |
| `server_name` | `lpcg-api.tosinamuda.com` | `lpcg-staging-api.tosinamuda.com` |
| `nginx_site` | `plan-to-tutor` | `plan-to-tutor-staging` |
| TLS certificate | `/etc/letsencrypt/live/lpcg-api.tosinamuda.com/` | `/etc/letsencrypt/live/lpcg-staging-api.tosinamuda.com/` |
| `db_backup_unit` | `db-backup`, at 02:30 | `ptt-db-backup-staging`, at 02:45 |
| Dumps | `/opt/lpcg/backups/mysql` | `/opt/lpcg-staging/backups/mysql` |
| `.env` | `/opt/lpcg/apps/backend/.env` | `/opt/lpcg-staging/apps/backend/.env` |
| Logs | `journalctl -u ptt-api` | `journalctl -u ptt-api-staging` |
| Vault | `greencloud.vault.yml` | `greencloud-staging.vault.yml` |
| Frontend | `https://lpcg.tosinamuda.com` | `https://lpcg-staging.tosinamuda.com` |

[`host_vars/greencloud.yml`](host_vars/greencloud.yml) and [`host_vars/greencloud-staging.yml`](host_vars/greencloud-staging.yml) set these names.
The defaults in [`group_vars/all.yml`](group_vars/all.yml) are the production names.

The play protects each instance:

- A run deploys one instance. Always name it with `-l`.
- A production run stops unless `release_tag` is a tag like `v2026.09.26` or `v2026.09.26.1` that exists on origin.
- The play loads the vault of the host that it deploys, so an instance cannot get the secrets of another instance.
- The server tasks (packages, MySQL, nginx, certbot) only install what is missing. They do not restart MySQL.
- Only production stops and deletes the retired units `ptt-worker`, `ptt-flower`, `ptt-relay` and `ptt-relay.timer`.

## Install

On the control machine:

```bash
cd deploy/ansible
ansible-galaxy collection install -r requirements.yml
cp inventory.example.ini inventory.ini   # add ansible_ssh_private_key_file if you need it
```

## Configure

Each instance has a vault file `<host>.vault.yml` in `deploy/ansible`.
Git ignores `*.vault.yml`. Do not commit a vault file.
The play loads the file for the host, and stops if the file is missing.

| Variable | Value |
| --- | --- |
| `db_password` | The password of the instance database user. Use a different password for each instance. |
| `bedrock_mantle_api_key` | The generator key. Copy `BEDROCK_MANTLE_API_KEY` from `apps/backend/.env`. The API does not start without it. |
| `deepseek_api_key` | The engine key. Copy `DEEPSEEK_API_KEY` from `apps/backend/.env`. Every plugin writer runs on DeepSeek, so none works without it. |
| `download_link_secret` | Any long random string, such as `openssl rand -hex 32`. It signs the download links for slide decks; a link made on one machine is not valid on another. |
| `certbot_email` | The address Let's Encrypt sends certificate notices to |
| `hf_token` | A Hugging Face read token with access to the gated `tosinamuda/ng-jss1-math-*` datasets |
| `cors_allowed_origins` | The frontend origins of the instance (see [CORS](#cors)) |
| `db_backup_deploy_key` | Only with `db_backup_git_repo` (see [Database backups](#database-backups)) |

Use the same vault password for all vault files:

```bash
cd deploy/ansible
ansible-vault create greencloud-staging.vault.yml --vault-password-file ~/.config/lpcg/vault_pass.txt
ansible-vault view greencloud-staging.vault.yml --vault-password-file ~/.config/lpcg/vault_pass.txt
```

```yaml
# greencloud-staging.vault.yml
db_password: "..."            # openssl rand -hex 24
bedrock_mantle_api_key: "..."
hf_token: "..."
certbot_email: "..."          # the address Let's Encrypt sends expiry notices to
cors_allowed_origins: "https://*.lpcg.pages.dev"
```

If a plaintext copy of a vault file was ever exposed, rotate its `db_password`.

These variables have defaults that you can change in `host_vars/<host>.yml`:

| Variable | Default | Controls |
| --- | --- | --- |
| `deploy_env` | `production` | `production` deploys a release tag only |
| `repo_url`, `repo_branch` | `git@github.com:tosinamuda/lpcg.git`, `main` | The code that the server pulls |
| `release_tag` | `""` | The tag to deploy. Production requires it. On another instance, it replaces `repo_branch`. |
| `app_user`, `app_root` | `ptt`, `/opt/plan-to-tutor` | The service user and the checkout |
| `api_service`, `nginx_site`, `db_backup_unit` | `ptt-api`, `plan-to-tutor`, `db-backup` | The unit, vhost and backup names of the instance |
| `db_name`, `db_user` | `plan_to_tutor` | The instance database and its user |
| `backend_port` | `8000` | The localhost port of the API |
| `server_name` | `$PTT_SERVER_NAME`, else `plan-to-tutor.example.com` | The DNS name or IP address of the instance |
| `api_public_port` | `8085` | The nginx port |
| `enable_tls`, `certbot_email` | `false`, `$PTT_CERTBOT_EMAIL` | TLS on `api_public_port` (see [TLS](#tls)) |
| `run_seeds` | `false` | The seed chain after the migrations |
| `retired_units` | the four Celery units | The units that the deploy stops and deletes. Set `[]` on a second instance. |
| `manage_app_user`, `manage_default_site` | `true` | Whether the play creates the user and disables the nginx default site |

### Git access on the server

The server pulls `repo_url` on each deploy, so push the branch or the tag first.
All instances on a server use the same read-only deploy key.
To give the app user a deploy key:

```bash
# On the server. <app_user> is ptt, or www-data on a shared host.
sudo -u <app_user> -H sh -c '
  mkdir -p -m 700 ~/.ssh
  ssh-keygen -t ed25519 -f ~/.ssh/lpcg_deploy -N "" -C lpcg-deploy
  printf "Host github.com\n  IdentityFile ~/.ssh/lpcg_deploy\n" >> ~/.ssh/config
  ssh-keyscan github.com >> ~/.ssh/known_hosts
  cat ~/.ssh/lpcg_deploy.pub'   # add this key in GitHub: repository > Settings > Deploy keys
```

### Add an instance

1. Copy `host_vars/greencloud-staging.yml` to `host_vars/<host>.yml`.
2. Change every name in the [Instances](#instances) table to a free value. Find the used ports with `ss -tlnH`.
3. Add `<host>` to `inventory.ini` with the same `ansible_host`.
4. Create `<host>.vault.yml`.
5. Add a DNS record for `server_name`.

## Deploy

Run the playbook from a checkout of the ref that you deploy.
The tasks then match the code on the server.
Replace `VAULT` with `--vault-password-file ~/.config/lpcg/vault_pass.txt`, or use `--ask-vault-pass`.

### Staging

```bash
git switch main && git pull
cd deploy/ansible
ansible-playbook site.yml -l greencloud-staging VAULT
```

On the first run, add `-e run_seeds=true`.

### Release to production

1. Deploy `main` to staging, and test it on `https://lpcg-staging.tosinamuda.com`.
2. Tag the commit and push the tag:

   ```bash
   git switch main && git pull
   TAG=v$(date +%Y.%m.%d)          # add .1, .2 for a second release on one day
   git tag -a "$TAG" -m "Release $TAG"
   git push origin "$TAG"
   ```

3. Deploy the API:

   ```bash
   git checkout "$TAG"
   cd deploy/ansible
   ansible-playbook site.yml -l greencloud -e release_tag="$TAG" VAULT
   ```

4. Deploy the frontend. Cloudflare Pages builds production from the `release` branch:

   ```bash
   git push origin "$TAG^{commit}:refs/heads/release"
   ```

5. Do a check of `https://lpcg.pages.dev` and `https://lpcg-api.tosinamuda.com/api/health`.
6. Run `git switch main`.

### Roll back production

1. Find the previous tag with `git tag --list 'v*' --sort=-creatordate`, and set `PREV` to it.
2. If the bad release added a file in `apps/backend/migrations/schema/versions`, downgrade the schema first.
   Do this while the bad release is still on the server:

   ```bash
   git checkout "$PREV" && (cd apps/backend && uv run alembic heads)   # the revision of PREV
   ssh root@<server-ip> "cd /opt/lpcg/apps/backend && sudo -u www-data /usr/local/bin/uv run alembic downgrade <revision>"
   ```

3. Deploy the previous tag:

   ```bash
   git checkout "$PREV"
   cd deploy/ansible
   ansible-playbook site.yml -l greencloud -e release_tag="$PREV" VAULT
   git push --force origin "$PREV^{commit}:refs/heads/release"
   ```

For a faster frontend rollback, open the Pages project, select **Deployments**, and select **Rollback** on the previous production deployment.

### What a deploy does

The roles in [`site.yml`](site.yml) run in this order:

1. The play checks that the run has one instance, that the vault loaded, and that production has a release tag.
2. `common` installs git, uv, the WeasyPrint libraries, and TeX with TikZ and `dvisvgm`.
3. `opencode` installs the release in `opencode_version` with the box's own npm, in `opencode_prefix`, and links it to `/usr/local/bin/opencode`. The engine's adapter refuses any other release. The role installs nothing when the release is already there.
4. `mysql` installs MySQL if it is missing, and creates the instance database and its user.
5. `backend` checks that `release_tag` exists on origin, pulls the code, writes `apps/backend/.env`, and runs `uv sync`.
6. `backend` stops and deletes the units in `retired_units`, if they exist.
7. `backend` runs these commands in `apps/backend`:

   ```bash
   uv run alembic upgrade head                                   # migrations/schema
   uv run python scripts/seed_all.py --no-migrate                # only with run_seeds=true
   uv run python -m scripts.seed_content_specifications          # adds new specification revisions
   uv run python -m scripts.seed_casbin_policies                 # adds new authorisation rows
   uv run python -m app.domains.content.plugins sync ../../plugins/<folder>                # installs or updates each plugin in content_plugins
   uv run python -m migrations.data.requeue_unfinished_work      # gives each unfinished generation a job
   ```

8. `backend` installs and starts `api_service`. It restarts the unit when the code, `.env` or the unit file changed.
9. `nginx` writes the vhost and, with `enable_tls: true`, gets the certificate.
10. `db_backup` installs the backup script and its timer.

A failed task stops the play before the restart.
Fix the cause, then run the playbook again.

### Seeds

[`scripts/seed_all.py`](../../apps/backend/scripts/seed_all.py) runs the seeds in order and stops at the first failure.
The last two steps are `seed_msc_study` and `seed_figures`.
Each seed is idempotent.
To run one seed on a live instance:

```bash
ssh <server> "cd <app_root>/apps/backend && sudo -u <app_user> PYTHONPATH=. /usr/local/bin/uv run python scripts/seed_msc_study.py"
```

- Run `seed_msc_study` when the study pins or the importer change.
  It fetches the two gated datasets at their pinned commits and checks each file against `PROVENANCE.json`.
  It keeps a current import and replaces an older one in one transaction.
- `seed_figures` draws each stored TikZ figure into SVG, and the API serves it from `/figures/<sha256>.svg`.
  Without TeX, a figure shows its caption.

## Operate

```bash
sudo systemctl status ptt-api ptt-api-staging nginx
sudo systemctl restart ptt-api-staging     # the API and its jobs
sudo journalctl -u ptt-api-staging -f      # API and job logs
curl https://lpcg-staging-api.tosinamuda.com/api/health
```

A stop or restart stops the running jobs and queues them again.
The ops panel shows each job, its runs, and its last error.

The job runner settings are in `JobsConfig` in [`apps/backend/src/app/config.py`](../../apps/backend/src/app/config.py):

| Setting | Value | Effect |
| --- | --- | --- |
| `slots` | 4 | Jobs that run at the same time, each in its own process |
| `heartbeat_seconds` | 30 | How often a running job renews its claim |
| `lease_seconds` | 120 | A job whose claim lapses runs again |
| `time_limit_seconds` | 7200 | The runner stops a job that runs longer, and queues it again |

A job runs again up to the number of runs that its kind allows.
Each slot adds one process that loads the app, so add slots only when the server has the memory.
Two instances need memory for two sets of slots.

## CORS

The frontend calls the API from a different origin.
`cors_allowed_origins` goes into `CORS_ALLOWED_ORIGINS` in `.env`, and [`app/cors.py`](../../apps/backend/src/app/cors.py) reads it.

- Separate the patterns with commas or spaces.
- Each pattern is an exact origin or contains `*`. The `*` matches one or more characters other than `/`.
- A pattern without a scheme matches http and https.
- The API always allows `http://localhost:<port>` and `http://127.0.0.1:<port>`.
- The API matches the whole origin, so `https://*.example.com` does not match `https://x.example.com.evil.com`.

| Instance | `cors_allowed_origins` |
| --- | --- |
| Production | `https://lpcg.pages.dev` |
| Staging | `https://lpcg-staging.tosinamuda.com, https://lpcg-staging.pages.dev, https://*.lpcg.pages.dev` |

## Frontend

Cloudflare Pages builds `apps/frontend` from git, in one Pages project for each instance.
A custom domain on a Pages project serves that project's production branch, so staging needs its own project.

| Project | Production branch | Custom domain | `VITE_API_BASE_URL` |
| --- | --- | --- | --- |
| `lpcg` | `release` | `lpcg.tosinamuda.com` | `https://lpcg-api.tosinamuda.com/api` |
| `lpcg-staging` | `main` | `lpcg-staging.tosinamuda.com` | `https://lpcg-staging-api.tosinamuda.com/api` |

Pages cannot build a tag, so production builds the `release` branch, and the release step moves `release` to the tag.
Staging builds every merge to `main`.

Both projects use the same build settings:

| Setting | Where | Value |
| --- | --- | --- |
| Build command | Settings > Builds | `npm run build` |
| Build output | Settings > Builds | `dist` |
| Root directory | Settings > Builds | `apps/frontend` |
| `VITE_API_BASE_URL` | Settings > Variables and Secrets | The API in the table above |

Vite puts `VITE_API_BASE_URL` into the build, so a change applies at the next build.

To build by hand:

```bash
# From the repository root
VITE_API_BASE_URL="https://lpcg-staging-api.tosinamuda.com/api" npm run build:frontend
wrangler pages deploy apps/frontend/dist --project-name lpcg --branch main
```

## TLS

When DNS points at the server, deploy with `enable_tls: true` (both greencloud instances set it):

1. nginx serves the ACME challenge for `server_name` on port 80.
2. certbot gets the certificate with the webroot HTTP-01 challenge, unless the certificate exists.
3. nginx serves HTTPS on `api_public_port` and redirects other port 80 requests to HTTPS.
4. `certbot.timer` renews the certificate, and a deploy hook then reloads nginx.

Port 80 must stay open to the internet, because each renewal uses it.

## Database backups

The `db_backup` role writes `<app_root>/backups/mysql/<db>-<UTC time>.sql.gz` each night.
It uses `mysqldump --single-transaction` and deletes dumps older than `db_backup_retention_days` (14).

```bash
sudo systemctl list-timers 'db-backup.timer' 'ptt-db-backup-staging.timer'   # the next runs
sudo systemctl start ptt-db-backup-staging.service   # a staging backup now
sudo journalctl -u ptt-db-backup-staging.service -e  # the log of the last run
ls -lh /opt/lpcg-staging/backups/mysql               # the dumps
gunzip < <dump>.sql.gz | mysql <db>                  # restore into an empty database
```

To push each dump to GitHub too:

1. Create a private GitHub repository, because the dumps contain real rows.
2. Make a key pair with `ssh-keygen -t ed25519 -f db_backup_key -N ""`.
3. Add the public key to the repository as a deploy key with write access.
4. Put the private key in the vault file as `db_backup_deploy_key`, as a YAML literal block.
5. Set `db_backup_git_repo` to the SSH URL of the repository in `host_vars/<host>.yml`.
6. Run the playbook.

## Test on a local VM

[Lima](https://lima-vm.io/) runs an Ubuntu 24.04 VM on macOS.
[`lima-prepare.sh`](lima-prepare.sh) points both instances at the VM, with their real `host_vars`.
It writes test vault files, and mirrors the branches and tags of your clone into the VM as `repo_url`.

```bash
brew install lima
limactl start ./deploy/lima/ptt-test.yaml   # the first start downloads the Ubuntu image

cd deploy/ansible
./lima-prepare.sh                           # set LIMA_HOME if your Lima home is not ~/.lima

ansible-playbook -i .lima/inventory.ini site.yml -l greencloud-staging -e enable_tls=false
ansible-playbook -i .lima/inventory.ini site.yml -l greencloud -e enable_tls=false -e release_tag=<a tag>

curl -H "Host: lpcg-staging-api.tosinamuda.com" http://localhost:8443/api/health
curl -H "Host: lpcg-api.tosinamuda.com" http://localhost:8443/api/health

limactl stop ptt-test
limactl delete ptt-test                     # the next start builds a new VM
```

The seed chain needs a real `hf_token` in `.lima/<host>.vault.yml`.

## Files

```
deploy/ansible/
├── site.yml                          # the play: checks, then common, opencode, mysql, backend, nginx, db_backup
├── group_vars/all.yml                # defaults for every host (production names)
├── host_vars/greencloud.yml          # production on the shared host
├── host_vars/greencloud-staging.yml  # staging on the same host
├── inventory.example.ini             # copy to inventory.ini
├── lima-prepare.sh                   # points both instances at the Lima VM
├── requirements.yml                  # Ansible collections
└── roles/
    ├── common/                       # packages, WeasyPrint libraries, TeX, uv, app user
    ├── opencode/                     # the engine's harness, pinned
    ├── mysql/                        # MySQL 9, the instance database and user
    ├── backend/                      # checkout, .env, migrations, seeds, API unit
    ├── nginx/                        # the API vhost and TLS
    └── db_backup/                    # the nightly dump and its timer
```
