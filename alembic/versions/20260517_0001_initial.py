"""initial

Revision ID: 20260517_0001
Revises: 
Create Date: 2026-05-17 00:01:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260517_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_users_id", "users", ["id"], unique=False)

    op.create_table(
        "letters",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("sender_name", sa.String(), nullable=False),
        sa.Column("sender_name_normalized", sa.String(), nullable=False),
        sa.Column("anonymous_hint", sa.String(), nullable=True),
        sa.Column("sender_ip", sa.String(), nullable=False),
        sa.Column("is_revealed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_letters_id", "letters", ["id"], unique=False)

    op.create_table(
        "guesses",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("letter_id", sa.Integer(), sa.ForeignKey("letters.id"), nullable=False),
        sa.Column("guessed_name", sa.String(), nullable=False),
        sa.Column("guessed_name_normalized", sa.String(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("letter_id", name="uq_guess_letter"),
    )
    op.create_index("ix_guesses_id", "guesses", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_guesses_id", table_name="guesses")
    op.drop_table("guesses")
    op.drop_index("ix_letters_id", table_name="letters")
    op.drop_table("letters")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
