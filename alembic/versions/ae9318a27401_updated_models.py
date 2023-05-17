"""updated models

Revision ID: ae9318a27401
Revises: df7feeabb63d
Create Date: 2023-05-10 03:03:41.245645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae9318a27401'
down_revision = 'df7feeabb63d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('my_model',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, 'question__tag__association', 'question', ['question_id'], ['id'])
    op.create_foreign_key(None, 'question__tag__association', 'question_tag', ['tag_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'question__tag__association', type_='foreignkey')
    op.drop_constraint(None, 'question__tag__association', type_='foreignkey')
    op.drop_table('my_model')
    # ### end Alembic commands ###
