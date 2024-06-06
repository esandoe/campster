"""Add is_pending to user model

Revision ID: cab89f782cfe
Revises: 7f52175dc6b4
Create Date: 2024-06-06 23:08:12.967104

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cab89f782cfe"
down_revision = "7f52175dc6b4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(sa.Column("is_pending", sa.Boolean(), nullable=True))

    # ### end Alembic commands ###

    # To enforce a NOT NULL constraint, we need to set all existing users to not pending first
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.execute("UPDATE user SET is_pending = false")
        batch_op.alter_column("is_pending", nullable=False)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("is_pending")

    # ### end Alembic commands ###
