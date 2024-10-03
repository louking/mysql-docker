"""set to match pre-docker members 1.6.7

Revision ID: 40d6c125c595
Revises: 593fba3d6616
Create Date: 2024-10-02 10:28:25.460049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40d6c125c595'
down_revision = '593fba3d6616'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    pass


def downgrade_():
    pass


def upgrade_users():
    pass


def downgrade_users():
    pass

