"""Pin relationships updated

Revision ID: 8b73c1f0ac5e
Revises: fcae341782d8
Create Date: 2022-06-24 12:21:19.116715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b73c1f0ac5e'
down_revision = 'fcae341782d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('like_pin_id_fkey', 'like', type_='foreignkey')
    op.create_foreign_key(None, 'like', 'pin', ['pin_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('save_pin_pin_id_fkey', 'save_pin', type_='foreignkey')
    op.create_foreign_key(None, 'save_pin', 'pin', ['pin_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('save_pin_board_pin_id_fkey', 'save_pin_board', type_='foreignkey')
    op.create_foreign_key(None, 'save_pin_board', 'pin', ['pin_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'save_pin_board', type_='foreignkey')
    op.create_foreign_key('save_pin_board_pin_id_fkey', 'save_pin_board', 'pin', ['pin_id'], ['id'])
    op.drop_constraint(None, 'save_pin', type_='foreignkey')
    op.create_foreign_key('save_pin_pin_id_fkey', 'save_pin', 'pin', ['pin_id'], ['id'])
    op.drop_constraint(None, 'like', type_='foreignkey')
    op.create_foreign_key('like_pin_id_fkey', 'like', 'pin', ['pin_id'], ['id'])
    # ### end Alembic commands ###