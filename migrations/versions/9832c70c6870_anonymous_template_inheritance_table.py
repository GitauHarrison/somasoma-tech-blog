"""anonymous template inheritance table

Revision ID: 9832c70c6870
Revises: 618e1a139ab4
Create Date: 2021-12-23 16:21:16.137741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9832c70c6870'
down_revision = '618e1a139ab4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('comment', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_name'), ['name'], unique=False)

    op.create_table('template inheritance comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('template inheritance comment', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_template inheritance comment_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('template inheritance comment', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_template inheritance comment_timestamp'))

    op.drop_table('template inheritance comment')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_name'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###
