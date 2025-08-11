"""initial with multiple majors support

Revision ID: ac2a254fbacc
Revises:
Create Date: 2025-08-11 11:01:06.084475

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ac2a254fbacc"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "members",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("first_name", sa.String(128), nullable=False),
        sa.Column("last_name", sa.String(128), nullable=False),
        sa.Column("email", sa.String(128), nullable=False, unique=True),
        sa.Column("student_id", sa.String(30), nullable=False, unique=True),
        sa.Column("discord_id", sa.String(128), nullable=True, unique=True),
    )
    op.create_table(
        "periods",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("start_date", sa.Date, nullable=False),
        sa.Column("end_date", sa.Date, nullable=False),
    )
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(64), nullable=False, unique=True),
    )
    op.create_table(
        "majors",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(128), nullable=False, unique=True),
    )
    op.create_table(
        "memberships",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("member_id", sa.Integer, nullable=False),
        sa.Column("period_id", sa.Integer, nullable=False),
        sa.Column("fee_paid", sa.Boolean, nullable=False),
        sa.Column("tshirt_received", sa.Boolean, nullable=False),
    )
    op.create_table(
        "membership_roles",
        sa.Column("membership_id", sa.Integer, primary_key=True),
        sa.Column("role_id", sa.Integer, primary_key=True),
    )
    op.create_table(
        "membership_majors",
        sa.Column("membership_id", sa.Integer, primary_key=True),
        sa.Column("major_id", sa.Integer, primary_key=True),
    )
    op.create_foreign_key(None, "memberships", "members", ["member_id"], ["id"])
    op.create_foreign_key(None, "memberships", "periods", ["period_id"], ["id"])
    op.create_foreign_key(
        None, "membership_roles", "memberships", ["membership_id"], ["id"]
    )
    op.create_foreign_key(None, "membership_roles", "roles", ["role_id"], ["id"])
    op.create_foreign_key(
        None, "membership_majors", "memberships", ["membership_id"], ["id"]
    )
    op.create_foreign_key(None, "membership_majors", "majors", ["major_id"], ["id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("membership_majors")
    op.drop_table("membership_roles")
    op.drop_table("memberships")
    op.drop_table("members")
    op.drop_table("periods")
    op.drop_table("roles")
    op.drop_table("majors")
