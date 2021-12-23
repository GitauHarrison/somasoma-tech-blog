"""allowed status field in update blog model

Revision ID: ac34cfce713b
Revises: 33087384e06e
Create Date: 2021-12-23 23:26:04.983633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac34cfce713b'
down_revision = '33087384e06e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('update course', schema=None) as batch_op:
        batch_op.add_column(sa.Column('allowed_status', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('update course', schema=None) as batch_op:
        batch_op.drop_column('allowed_status')

    # ### end Alembic commands ###
