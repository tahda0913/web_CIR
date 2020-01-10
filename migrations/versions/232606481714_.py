"""empty message

Revision ID: 232606481714
Revises: e086edcb8e38
Create Date: 2020-01-10 13:55:17.978691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '232606481714'
down_revision = 'e086edcb8e38'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('crisis_team_responses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('response', sa.String(length=400), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('crisis_team_responses')
    # ### end Alembic commands ###
