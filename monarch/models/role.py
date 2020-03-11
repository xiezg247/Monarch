from sqlalchemy import Column, Integer, String, JSON, Boolean
from sqlalchemy.orm import relationship

from monarch.models.base import Base, TimestampMixin


class Role(Base, TimestampMixin):
    """角色表"""

    __tablename__ = "role"

    id = Column(
        Integer(), nullable=False, autoincrement=True, primary_key=True, comment="角色ID",
    )

    company_id = Column(Integer, nullable=False, comment="公司ID")
    name = Column(String(32), nullable=False, comment="角色名称")
    description = Column(String(500), comment="角色描述")
    is_admin = Column(Boolean(), nullable=False, default=False, comment="是否管理员")

    users = relationship(
        "User",
        secondary="user_role",
        primaryjoin="Role.id==UserRole.role_id",
        secondaryjoin="User.id==UserRole.user_id",
    )

    @classmethod
    def get_admin_role_by_company_id(cls, company_id, is_admin=True, deleted=False):
        return cls.query.filter(
            cls.company_id == company_id,
            cls.is_admin == is_admin,
            cls.deleted == deleted
        ).first()


class RolePermission(Base, TimestampMixin):
    """角色权限表"""
    __tablename__ = "role_permission"

    id = Column(
        Integer(), nullable=False, autoincrement=True, primary_key=True, comment="角色权限ID",
    )

    role_id = Column(Integer, nullable=False, comment="角色ID")
    company_id = Column(Integer, nullable=False, comment="公司ID")
    app_id = Column(Integer, nullable=False, comment="应用ID")
    permission = Column(JSON, nullable=False, default=[], comment="角色菜单权限")

    @classmethod
    def get_by_role_company_app_id(cls, role_id, company_id, app_id, deleted=False):
        return cls.query.filter(
            cls.role_id == role_id,
            cls.app_id == app_id,
            cls.company_id == company_id,
            cls.deleted == deleted
        ).first()
