"""JSON tags

Revision ID: 24558a4759bc
Revises: 
Create Date: 2023-01-29 18:44:06.563758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24558a4759bc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cs_nutri_recipes', schema=None) as batch_op:
        batch_op.alter_column('tags',
               existing_type=sa.TEXT(),
               nullable=True)

    with op.batch_alter_table('de_nutri_recipes', schema=None) as batch_op:
        batch_op.alter_column('tags',
               existing_type=sa.TEXT(),
               nullable=True)

    with op.batch_alter_table('en_nutri_recipes', schema=None) as batch_op:
        batch_op.alter_column('tags',
               existing_type=sa.TEXT(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('en_nutri_recipes', schema=None) as batch_op:
        batch_op.alter_column('tags',
               existing_type=sa.TEXT(),
               nullable=False)

    with op.batch_alter_table('de_nutri_recipes', schema=None) as batch_op:
        batch_op.alter_column('tags',
               existing_type=sa.TEXT(),
               nullable=False)

    with op.batch_alter_table('cs_nutri_recipes', schema=None) as batch_op:
        batch_op.alter_column('tags',
               existing_type=sa.TEXT(),
               nullable=False)

    # ### end Alembic commands ###
