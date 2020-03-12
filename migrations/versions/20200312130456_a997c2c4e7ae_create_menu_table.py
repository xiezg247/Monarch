"""create menu table

Revision ID: a997c2c4e7ae
Revises: 403a60e7f113
Create Date: 2020-03-12 13:04:56.825875

"""
from alembic import op
from sqlalchemy import Integer, String, Column, DateTime, Boolean
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'a997c2c4e7ae'
down_revision = '403a60e7f113'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "menu",
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
        Column(
            "id",
            Integer(),
            nullable=False,
            autoincrement=True,
            primary_key=True,
            comment="菜单ID",
        ),
        Column("name", String(32), nullable=False, comment="菜单名称"),
        Column("parent_id", Integer, nullable=False, default=0, comment="父级菜单ID"),
    )


def downgrade():
    op.drop_table("menu")
