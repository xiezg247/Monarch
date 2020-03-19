"""alter company add column

Revision ID: 406cca548eaf
Revises: e5e0b0725286
Create Date: 2020-03-12 17:47:39.110861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '406cca548eaf'
down_revision = 'e5e0b0725286'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("company_app", sa.Column("init_status", sa.Integer, nullable=False, comment="初始化状态：1 成功 2 失败"))


def downgrade():
    op.drop_column("company_app", "init_status")
