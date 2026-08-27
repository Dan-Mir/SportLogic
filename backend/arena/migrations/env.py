from __future__ import annotations

from alembic import context


def run_migrations_offline() -> None:
    cfg = context.config
    url = cfg.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table=cfg.get_main_option("version_table"),
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    from sqlalchemy import create_engine

    cfg = context.config
    url = cfg.get_main_option("sqlalchemy.url")
    connectable = create_engine(url)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            version_table=cfg.get_main_option("version_table"),
        )
        with context.begin_transaction():
            context.run_migrations()
