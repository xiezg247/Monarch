"""init tables

Revision ID: 403a60e7f113
Revises:
Create Date: 2020-03-10 09:54:40.414155

"""
from datetime import datetime
from alembic import op
from sqlalchemy import String, Column, DateTime, Boolean, Integer


# revision identifiers, used by Alembic.
revision = '403a60e7f113'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "admin_user",
        Column(
            "created_at",
            DateTime(),
            nullable=False,
            default=datetime.now,
            comment="创建时间",
        ),
        Column(
            "updated_at",
            DateTime(),
            nullable=False,
            default=datetime.now,
            onupdate=datetime.now,
            comment="更新时间",
        ),
        Column("deleted", Boolean(), nullable=False, default=False, comment="是否删除"),
        Column("id", String(32), nullable=False, primary_key=True, comment="管理员ID"),
        Column("account", String(32), nullable=False, comment="账号"),
        Column("password", String(128), nullable=False, comment="密码"),
        Column('company_id', Integer(), nullable=False, comment="公司ID"),

    )
    op.create_index('uq_account_deleted', 'user', ['account', 'deleted'], unique=True)
    op.create_index('idx_company_id', 'user', ['company_id'], unique=False)


def downgrade():
    op.drop_table("admin_user")
