"""add relation Board  table

Revision ID: 6416d8979792
Revises: b860c485f002
Create Date: 2022-06-17 16:19:45.238949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6416d8979792'
down_revision = 'b860c485f002'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('board',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('save_pin', sa.Column('board_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'save_pin', 'board', ['board_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'save_pin', type_='foreignkey')
    op.drop_column('save_pin', 'board_id')
    op.drop_table('board')
    # ### end Alembic commands ###
