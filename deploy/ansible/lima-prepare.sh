#!/usr/bin/env bash
# Makes the running Lima VM a dress-rehearsal target for BOTH instances:
#   .lima/inventory.ini       greencloud and greencloud-staging, both pointing at the VM
#   .lima/<host>.vault.yml    test secrets, written once
#   /srv/lpcg.git in the VM   a mirror of this clone's branches and tags (repo_url)
# The hosts keep their real names, so the rehearsal applies the real host_vars.
# Run it again after new commits to refresh the mirror.
set -euo pipefail

VM="${VM:-ptt-test}"
LIMA_HOME="${LIMA_HOME:-$HOME/.lima}"
SSH_CONFIG="$LIMA_HOME/$VM/ssh.config"
SSH_HOST="lima-$VM"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUT="$SCRIPT_DIR/.lima"

if [ ! -f "$SSH_CONFIG" ] || ! ssh -F "$SSH_CONFIG" "$SSH_HOST" true 2>/dev/null; then
  echo "ERROR: VM '$VM' is not reachable through $SSH_CONFIG. Start it first:"
  echo "  limactl start ./deploy/lima/ptt-test.yaml"
  exit 1
fi

mkdir -p "$OUT"
cat > "$OUT/inventory.ini" <<EOF
# Written by lima-prepare.sh. Both instances run on the Lima VM '$VM'.
# Host vars sit on the host lines, because [app:vars] ranks below group_vars/all.yml.
[app]
greencloud ansible_host=$SSH_HOST repo_url=/srv/lpcg.git vault_file=$OUT/greencloud.vault.yml
greencloud-staging ansible_host=$SSH_HOST repo_url=/srv/lpcg.git vault_file=$OUT/greencloud-staging.vault.yml

[app:vars]
ansible_ssh_common_args="-F $SSH_CONFIG"
EOF

for host in greencloud greencloud-staging; do
  vault="$OUT/$host.vault.yml"
  [ -f "$vault" ] && continue
  cat > "$vault" <<EOF
# Test values for the Lima VM only. Set hf_token to a real read token to run the seed chain.
db_password: "$(openssl rand -hex 16)"
bedrock_mantle_api_key: "test"
hf_token: ""
cors_allowed_origins: "http://localhost:3000"
EOF
  chmod 600 "$vault"
done

BUNDLE="$(mktemp -d)/lpcg.bundle"
git -C "$SCRIPT_DIR" bundle create "$BUNDLE" --branches --tags
scp -q -F "$SSH_CONFIG" "$BUNDLE" "$SSH_HOST:/tmp/lpcg.bundle"
rm -f "$BUNDLE"
# The app user clones from a root-owned mirror, which git refuses without safe.directory.
# The VM copies what greencloud has before the play runs: nginx, and a uv cache that
# www-data owns in its home (/var/www), because the other apps run uv as www-data.
ssh -F "$SSH_CONFIG" "$SSH_HOST" '
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq nginx >/dev/null
  sudo install -d -o www-data -g www-data /var/www/.cache
  sudo rm -rf /srv/lpcg.git
  sudo git clone --quiet --mirror /tmp/lpcg.bundle /srv/lpcg.git
  sudo git config --system --replace-all safe.directory /srv/lpcg.git
  rm -f /tmp/lpcg.bundle'

echo "Ready. Deploy from deploy/ansible, one instance per run:"
echo "  ansible-playbook -i .lima/inventory.ini site.yml -l greencloud-staging -e enable_tls=false"
echo "  ansible-playbook -i .lima/inventory.ini site.yml -l greencloud -e enable_tls=false -e release_tag=<tag>"
