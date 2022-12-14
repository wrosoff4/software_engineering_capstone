"""empty message

Revision ID: 12f8ef40a168
Revises: dac0f61c2c61
Create Date: 2021-11-19 11:44:30.520377

"""
from alembic import op
import sqlalchemy as sa
from incident_app.populate import populate


# revision identifiers, used by Alembic.
revision = '12f8ef40a168'
down_revision = 'dac0f61c2c61'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('incident', schema=None) as batch_op:
        batch_op.alter_column('photos_taken',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    populate()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('incident', schema=None) as batch_op:
        batch_op.alter_column('photos_taken',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###
