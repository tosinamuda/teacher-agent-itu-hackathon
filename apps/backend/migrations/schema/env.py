from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool, text
from sqlalchemy.schema import SchemaItem

# override=False so an external DATABASE_URL (e.g. the test DB during pytest)
# wins over the dev value in .env. Standard env-var precedence: ambient
# environment beats project defaults. Production deploys set DATABASE_URL
# explicitly anyway; .env remains the local-dev fallback.
load_dotenv(override=False)

from app.db.config import get_database_url  # noqa: E402
from app.db.metadata import target_metadata  # noqa: E402

#: Tables the models do not describe: the Casbin adapter owns this one.
_IGNORED_TABLES = frozenset({"casbin_rule"})
#: Indexes created on a ``created_at DESC`` expression, which a comparison of the models with
#: MySQL reports as changed whatever the schema holds.
_IGNORED_INDEXES = frozenset(
    {
        "ix_artefact_plans_kind_scope_plan_version_created_at",
        "ix_artefacts_kind_scope_plan_version_created_at",
        "ix_exit_ticket_submissions_student_plan_version_created_at",
        "ix_student_pack_generations_plan_student_created",
    }
)


def include_object(
    obj: SchemaItem, name: str | None, type_: str, reflected: bool, compare_to: SchemaItem | None
) -> bool:
    """Leave out of ``alembic check`` and autogenerate what no migration can bring in line."""
    if type_ == "table":
        return name not in _IGNORED_TABLES
    if type_ == "index":
        owner = getattr(getattr(obj, "table", None), "name", None)
        return name not in _IGNORED_INDEXES and owner not in _IGNORED_TABLES
    return True


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", get_database_url())


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Some revision IDs exceed 32 chars, but Alembic's auto-created
        # ``alembic_version.version_num`` column is only ``VARCHAR(32)`` and
        # silently rejects longer writes. Pre-create the table with a wide enough
        # column so a fresh deploy survives the upgrade.
        connection.execute(
            text(
                "CREATE TABLE IF NOT EXISTS alembic_version ("
                "version_num VARCHAR(255) NOT NULL, "
                "CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num))"
            )
        )
        connection.commit()

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
