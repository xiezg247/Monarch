"""init tables

Revision ID: 403a60e7f113
Revises:
Create Date: 2020-03-10 09:54:40.414155

"""
from datetime import datetime
from alembic import op
from sqlalchemy import Index, Integer, String, Column, JSON, DateTime, Boolean
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '403a60e7f113'
down_revision = None
branch_labels = None
depends_on = None



CREATE_OAUTH_APP = """
CREATE TABLE `o_auth_app` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NOT NULL DEFAULT NOW(),
  `updated_at` timestamp NOT NULL DEFAULT NOW(),
  `deleted` boolean NOT NULL DEFAULT FALSE ,
  `name` varchar(64) NOT NULL,
  `client_id` varchar(36) NOT NULL,
  `client_secret` varchar(36) NOT NULL,
  `description` varchar(128) NOT NULL,
  `homepage` varchar(128) NOT NULL,
  `redirect_url` varchar(128) NOT NULL,
  `status` bigint(20) NOT NULL DEFAULT '0',
  `scopes` bigint(20) NOT NULL DEFAULT '0',
  `white_list` tinyint(1) DEFAULT '0' NOT NULL,
  `is_default` tinyint(1) DEFAULT '0' NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_client_id` (`client_id`),
  UNIQUE KEY `uq_client_secret` (`client_secret`),
  KEY `idx_o_auth_apps_deleted` (`deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"""

CREATE_OAUTH_AUTHORIZE = """
CREATE TABLE `o_auth_authorize` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NOT NULL DEFAULT NOW(),
  `updated_at` timestamp NOT NULL DEFAULT NOW(),
  `deleted` boolean NOT NULL DEFAULT FALSE ,
  `app_id` int(10) unsigned NOT NULL,
  `code` varchar(36) NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `scopes` bigint(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `idx_o_auth_authorizes_deleted` (`deleted`),
  KEY `idx_o_auth_authorizes_app_id` (`app_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"""

CREATE_OAUTH_TOKEN = """
CREATE TABLE `o_auth_token` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NOT NULL DEFAULT NOW(),
  `updated_at` timestamp NOT NULL DEFAULT NOW(),
  `deleted` boolean NOT NULL DEFAULT FALSE ,
  `app_id` int(10) unsigned NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `access_token` varchar(36) NOT NULL,
  `refresh_token` varchar(36) NOT NULL,
  `scopes` bigint(20) NOT NULL DEFAULT '0',
  `type` varchar(16) NOT NULL DEFAULT 'Bearer',
  PRIMARY KEY (`id`),
  UNIQUE KEY `access_token` (`access_token`),
  UNIQUE KEY `refresh_token` (`refresh_token`),
  UNIQUE KEY `idx_app_id_user_id` (`app_id`,`user_id`),
  KEY `idx_o_auth_tokens_deleted` (`deleted`),
  KEY `idx_o_auth_tokens_app_id` (`app_id`),
  KEY `idx_o_auth_tokens_user_id` (`user_id`)
) ENGINE=Innodb DEFAULT CHARSET=utf8mb4
"""


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text(CREATE_OAUTH_APP))
    conn.execute(sa.text(CREATE_OAUTH_AUTHORIZE))
    conn.execute(sa.text(CREATE_OAUTH_TOKEN))

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
    )

    op.create_table(
        "company",
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
            comment="公司ID",
        ),
        Column("code", String(32), nullable=False, comment="公司编码"),
        Column("name", String(128), nullable=True, comment="公司名称"),
        Column("expired_at", DateTime(), default=datetime.now, comment="到期日期"),
        Column("remark", String(255), nullable=True, comment="企业描述"),
        Column("status", Integer, nullable=False, default=0, comment="开启状态"),
    )

    op.create_table(
        "company_admin_user",
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
            comment="公司管理负责人ID",
        ),
        Column("company_id", Integer, nullable=False, comment="公司ID"),
        Column(
            "admin_user_id", String(32), nullable=False, default=None, comment="管理负责人ID"
        ),
    )

    op.create_table(
        "company_app",
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
            comment="公司应用ID",
        ),
        Column("company_id", Integer, nullable=False, comment="公司ID"),
        Column("app_id", Integer, nullable=False, default=0, comment="应用ID"),
        Column("status", Integer, nullable=False, default=0, comment="状态"),
        Column("expired_at", DateTime(), default=datetime.now, comment="到期日期"),
    )

    op.create_table(
        "app_menu",
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
            comment="自增长ID",
        ),
        Column("app_id", Integer, nullable=False, default=0, comment="应用ID"),
        Column("name", String(32), nullable=False, comment="菜单名称"),
        Column("parent_id", String(32), nullable=False, default="", comment="父级菜单ID"),
        Column("menu_id", String(32), nullable=False, default="", comment="菜单ID"),
        Column("remark", String(128), nullable=False, comment="备注"),
        Column("route_name", String(128), nullable=False, default="/", comment="路由")
    )

    op.create_table(
        "company_robot",
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
            comment="公司机器人配置ID",
        ),
        Column("company_id", Integer, nullable=False, comment="公司ID"),
        Column("name", String(128), nullable=False, default=None, comment="机器人名称"),
        Column("robot_url", String(255), nullable=True, default=None, comment="机器人地址"),
        Column(
            "robot_version", String(128), nullable=True, default=None, comment="机器人版本"
        ),
        Column("robot_key", String(128), default=None, comment="机器人对接key"),

        Column("status", Integer, nullable=False, default=0, comment="状态"),
    )

    op.create_table(
        "user",
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

        Column("id", String(32), nullable=False, primary_key=True, comment="客服ID"),
        Column("company_id", Integer, nullable=False, comment="公司ID"),
        Column("account", String(32), nullable=False, comment="账号"),
        Column("password", String(128), nullable=False, comment="密码"),
        Column("username", String(32), nullable=False, comment="用户姓名"),
        Column("nickname", String(64), nullable=True, comment="用户昵称"),
        Column("avatar", String(255), nullable=True, default=None, comment="用户头像"),
        Column("mobile", String(16), nullable=True, comment="手机号码"),
        Column("enabled", Boolean(), nullable=False, default=False, comment="是否禁止"),
        Index("idx_account_deleted", "account", "deleted", unique=True),
        Index("idx_company_id", "company_id"),
    )

    op.create_table(
        "user_role",
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
            comment="客服角色ID",
        ),
        Column("user_id", String(32), nullable=False, comment="客服ID"),
        Column("role_id", Integer, nullable=False, comment="角色ID"),
    )

    op.create_table(
        "role",
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
            comment="角色ID",
        ),
        Column("company_id", Integer, nullable=False, comment="公司ID"),
        Column("name", String(32), nullable=False, comment="角色名称"),
    )


def downgrade():
    op.drop_table("o_auth_app")
    op.drop_table("o_auth_authorize")
    op.drop_table("o_auth_token")

    op.drop_table("admin_user")
    op.drop_table("company")
    op.drop_table("company_admin_user")

    op.drop_table("company_app")
    op.drop_table("app_menu")
    op.drop_table("company_robot")

    op.drop_table("user")
    op.drop_table("user_role")
    op.drop_table("role")
