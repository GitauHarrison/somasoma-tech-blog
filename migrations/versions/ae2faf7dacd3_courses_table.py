"""courses table

Revision ID: ae2faf7dacd3
Revises: bac8179ceaf3
Create Date: 2021-12-23 21:33:52.661625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae2faf7dacd3'
down_revision = 'bac8179ceaf3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('update course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_image', sa.String(length=140), nullable=True),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('overview', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('next_class_date', sa.String(length=140), nullable=True),
    sa.Column('link', sa.String(length=140), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('update course', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_update course_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_update course_title'), ['title'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('update course', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_update course_title'))
        batch_op.drop_index(batch_op.f('ix_update course_timestamp'))

    op.drop_table('update course')
    # ### end Alembic commands ###
