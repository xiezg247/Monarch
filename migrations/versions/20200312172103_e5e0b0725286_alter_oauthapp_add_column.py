"""alter OAuthApp add column

Revision ID: e5e0b0725286
Revises: a997c2c4e7ae
Create Date: 2020-03-12 17:21:03.040023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5e0b0725286'
down_revision = 'a997c2c4e7ae'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("o_auth_app", sa.Column("init_url", sa.String(128), nullable=True, default="", comment="初始化URL"))


def downgrade():
    op.drop_column("o_auth_app", "init_url")
