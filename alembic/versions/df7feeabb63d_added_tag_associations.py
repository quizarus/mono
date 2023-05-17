"""added tag associations

Revision ID: df7feeabb63d
Revises: 4cbb416aaedb
Create Date: 2023-05-08 00:09:41.616890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df7feeabb63d'
down_revision = '4cbb416aaedb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question__tag__association',
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('question_id', 'tag_id')
    )
    op.create_table('question_tag',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('question_pack__tag__association',
    sa.Column('pack_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pack_id'], ['question_pack.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['question_tag.id'], ),
    sa.PrimaryKeyConstraint('pack_id', 'tag_id')
    )
    op.drop_constraint('question_pack_id_fkey', 'question', type_='foreignkey')
    op.create_foreign_key(None, 'question', 'question_pack', ['pack_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('question_answer_question_id_fkey', 'question_answer', type_='foreignkey')
    op.create_foreign_key(None, 'question_answer', 'question', ['question_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'question_answer', type_='foreignkey')
    op.create_foreign_key('question_answer_question_id_fkey', 'question_answer', 'question', ['question_id'], ['id'])
    op.drop_constraint(None, 'question', type_='foreignkey')
    op.create_foreign_key('question_pack_id_fkey', 'question', 'question_pack', ['pack_id'], ['id'])
    op.drop_table('question_pack__tag__association')
    op.drop_table('question_tag')
    op.drop_table('question__tag__association')
    # ### end Alembic commands ###
