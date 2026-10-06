from alembic import context

from arena.migrations.env import run_migrations_offline, run_migrations_online

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
