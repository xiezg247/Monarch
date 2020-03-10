"""后续把登录验证抽离出去"""
from monarch.models.base import Base, TimestampMixin
from sqlalchemy import Column, String, Integer, Boolean, Index

from monarch.utils.model import escape_like


class OAuthApp(Base, TimestampMixin):
    """应用"""

    __tablename__ = "o_auth_app"

    __table_args__ = (
        # 唯一索引
        Index("uq_client_id", "client_id", unique=True),
        Index("uq_client_secret", "client_secret", unique=True),
        # 普通索引
        Index("idx_o_auth_apps_deleted", "deleted"),
    )

    # status
    UNAPPROVED = 1  # 未审核
    APPROVED = 2  # 已审核

    id = Column(
        Integer(), nullable=False, autoincrement=True, primary_key=True, comment="应用ID",
    )

    name = Column(String(64), nullable=False, comment="应用名")
    client_id = Column(String(36), nullable=False, comment="分配给App的key")
    client_secret = Column(String(36), nullable=False, comment="分配给App的secret")
    description = Column(String(128), nullable=False, default=None, comment="描述")
    homepage = Column(String(128), nullable=False, default=None, comment="主页")
    redirect_url = Column(String(128), nullable=False, comment="重定向的URL")
    status = Column(Integer(), nullable=False, default=0, comment="App的审核状态，默认审核中")
    # 这一期暂不做限制
    scopes = Column(Integer(), nullable=False, default=0, comment="申请的权限的位图，默认无权限")
    white_list = Column(Boolean(), nullable=False, default=False, comment="是否是白名单")

    @classmethod
    def query_oauth_app(cls, name, deleted=False):
        query = cls.query.filter(
            cls.deleted == deleted,
        ).order_by(
            cls.created_at.desc()
        )
        if name is not None:
            query = query.filter(cls.name.like("%" + escape_like(name) + "%"))
        return query


class OAuthAuthorize(Base, TimestampMixin):
    """授权码"""
    __tablename__ = "o_auth_authorize"

    __table_args__ = (
        # 普通索引
        Index("idx_o_auth_authorizes_deleted", "deleted"),
        Index("idx_o_auth_authorizes_app_id", "app_id"),
    )

    id = Column(
        Integer(), nullable=False, autoincrement=True, primary_key=True, comment="授权码ID",
    )

    app_id = Column(Integer(), nullable=False, default=0, comment="申请的权限的位图，默认无权限")
    user_id = Column(String(36), nullable=False, comment="用户ID")
    code = Column(String(36), nullable=False, comment="authorize code")
    scopes = Column(Integer(), nullable=False, default=0, comment="申请的权限的位图，默认无权限")


class OAuthToken(Base, TimestampMixin):
    """授权"""
    __tablename__ = "o_auth_token"

    __table_args__ = (
        # 唯一索引
        Index("uq_access_token", "access_token", unique=True),
        Index("uq_refresh_token", "refresh_token", unique=True),
        Index("uq_app_id_user_id", "app_id", "user_id", unique=True),
        # 普通索引
        Index("idx_o_auth_tokens_deleted", "deleted"),
        Index("idx_o_auth_tokens_app_id", "app_id"),
        Index("idx_o_auth_tokens_user_id", "user_id"),
    )

    id = Column(
        Integer(), nullable=False, autoincrement=True, primary_key=True, comment="授权ID",
    )

    app_id = Column(Integer(), nullable=False, default=0, comment="申请的权限的位图，默认无权限")
    user_id = Column(String(36), nullable=False, comment="用户ID")
    access_token = Column(String(36), nullable=False, comment="authorize code")
    refresh_token = Column(String(36), nullable=False, comment="authorize code")
    scopes = Column(Integer(), nullable=False, default=0, comment="申请的权限的位图，默认无权限")
    type = Column(String(16), nullable=False, default="Bearer", comment="token type，默认为Bearer")
