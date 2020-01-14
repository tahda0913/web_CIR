"""school lookup table

Revision ID: 6bf24c471f9a
Revises: 940037b6da96
Create Date: 2020-01-10 10:25:34.755580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bf24c471f9a'
down_revision = '940037b6da96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('school_lookup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('school_name', sa.String(length=200), nullable=True),
    sa.Column('dist_list', sa.String(length=600), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('school_lookup')
    # ### end Alembic commands ###