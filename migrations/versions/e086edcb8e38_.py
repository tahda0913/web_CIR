"""empty message

Revision ID: e086edcb8e38
Revises: 6bf24c471f9a
Create Date: 2020-01-10 12:03:39.171369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e086edcb8e38'
down_revision = '6bf24c471f9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('incident_lookup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('incident_type', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('incident_lookup')
    # ### end Alembic commands ###
