"""allowed status field in update blog model

Revision ID: c52f367b93e6
Revises: ac34cfce713b
Create Date: 2021-12-24 00:07:44.794034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c52f367b93e6'
down_revision = 'ac34cfce713b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('update blog', schema=None) as batch_op:
        batch_op.add_column(sa.Column('allowed_status', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('update blog', schema=None) as batch_op:
        batch_op.drop_column('allowed_status')

    # ### end Alembic commands ###