"""allowed status field in student stories model

Revision ID: 5cedcacbc59c
Revises: 370f980a9cfa
Create Date: 2021-12-24 00:10:10.785935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cedcacbc59c'
down_revision = '370f980a9cfa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('update student stories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('allowed_status', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('update student stories', schema=None) as batch_op:
        batch_op.drop_column('allowed_status')

    # ### end Alembic commands ###