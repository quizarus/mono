"""added new table 'answer', relations answer -> question

Revision ID: 4cbb416aaedb
Revises: 78052010215a
Create Date: 2023-05-07 23:00:23.013381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4cbb416aaedb'
down_revision = '78052010215a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question_answer',
    sa.Column('is_right', sa.Boolean(), nullable=False),
    sa.Column('text', sa.String(length=255), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('question_answer')
    # ### end Alembic commands ###
