"""Drop supplytarget name unique constraint

Because of SQLITE limitations which prevents us to remove a unique constraint,
we need to recreate the table and copy over data. This migration was created
manually (by AI!) to handle this case.

Revision ID: 9c62ffdb6669
Revises: 3346e4d1340e
Create Date: 2025-06-21 00:09:02.196190

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9c62ffdb6669"
down_revision = "3346e4d1340e"
branch_labels = None
depends_on = None


def upgrade():
    # 1. Create a new table without the unique constraint
    op.create_table(
        "supply_target_9c62ffdb6669",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("trip_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("target_quantity", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["trip_id"], ["trip.id"]),
    )
    # 2. Copy data from old table to new table
    op.execute(
        """
        INSERT INTO supply_target_9c62ffdb6669 (id, trip_id, name, target_quantity, created_at, updated_at)
        SELECT id, trip_id, name, target_quantity, created_at, updated_at FROM supply_target;
    """
    )
    # 3. Drop the old table
    op.drop_table("supply_target")
    # 4. Rename the new table to the original name
    op.rename_table("supply_target_9c62ffdb6669", "supply_target")


def downgrade():
    # 1. Recreate the table with the unique constraint
    op.create_table(
        "supply_target_9c62ffdb6669",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("trip_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("target_quantity", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["trip_id"], ["trip.id"]),
        sa.UniqueConstraint("name"),
    )
    # 2. Copy data back
    op.execute(
        """
        INSERT INTO supply_target_9c62ffdb6669 (id, trip_id, name, target_quantity, created_at, updated_at)
        SELECT id, trip_id, name, target_quantity, created_at, updated_at FROM supply_target;
    """
    )
    # 3. Drop the current table
    op.drop_table("supply_target")
    # 4. Rename back
    op.rename_table("supply_target_9c62ffdb6669", "supply_target")
