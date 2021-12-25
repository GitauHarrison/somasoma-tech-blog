"""all tables

Revision ID: 7708ec5e94c5
Revises: 
Create Date: 2021-12-25 10:02:34.490290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7708ec5e94c5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_admin_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_admin_username'), ['username'], unique=True)

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

    op.create_table('flask student stories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('student_image', sa.String(length=140), nullable=True),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('allowed_status', sa.Boolean(), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('flask student stories', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_flask student stories_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_flask student stories_username'), ['username'], unique=False)

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

    op.create_table('update blog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('blog_image', sa.String(length=140), nullable=True),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('link', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('allowed_status', sa.Boolean(), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('update blog', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_update blog_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_update blog_title'), ['title'], unique=False)

    op.create_table('update course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_image', sa.String(length=140), nullable=True),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('overview', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('next_class_date', sa.String(length=140), nullable=True),
    sa.Column('link', sa.String(length=140), nullable=True),
    sa.Column('allowed_status', sa.Boolean(), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('update course', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_update course_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_update course_title'), ['title'], unique=False)

    op.create_table('update events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('event_image', sa.String(length=140), nullable=True),
    sa.Column('event_date', sa.String(length=140), nullable=True),
    sa.Column('event_time', sa.String(length=140), nullable=True),
    sa.Column('location', sa.String(length=140), nullable=True),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('link', sa.String(length=140), nullable=True),
    sa.Column('allowed_status', sa.Boolean(), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('update events', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_update events_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_update events_title'), ['title'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('update events', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_update events_title'))
        batch_op.drop_index(batch_op.f('ix_update events_timestamp'))

    op.drop_table('update events')
    with op.batch_alter_table('update course', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_update course_title'))
        batch_op.drop_index(batch_op.f('ix_update course_timestamp'))

    op.drop_table('update course')
    with op.batch_alter_table('update blog', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_update blog_title'))
        batch_op.drop_index(batch_op.f('ix_update blog_timestamp'))

    op.drop_table('update blog')
    with op.batch_alter_table('template inheritance comment', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_template inheritance comment_timestamp'))

    op.drop_table('template inheritance comment')
    with op.batch_alter_table('flask student stories', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_flask student stories_username'))
        batch_op.drop_index(batch_op.f('ix_flask student stories_timestamp'))

    op.drop_table('flask student stories')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_name'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_admin_username'))
        batch_op.drop_index(batch_op.f('ix_admin_email'))

    op.drop_table('admin')
    # ### end Alembic commands ###
