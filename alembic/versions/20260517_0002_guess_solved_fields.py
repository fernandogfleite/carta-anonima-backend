"""guess solved fields

Revision ID: 20260517_0002
Revises: 20260517_0001
Create Date: 2026-05-17 00:02:00.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260517_0002"
down_revision = "20260517_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "letters",
        sa.Column(
            "is_solved", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
    )
    op.add_column(
        "letters", sa.Column("solved_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.drop_constraint("uq_guess_letter", "guesses", type_="unique")


def downgrade() -> None:
    op.create_unique_constraint("uq_guess_letter", "guesses", ["letter_id"])
    op.drop_column("letters", "solved_at")
    op.drop_column("letters", "is_solved")
