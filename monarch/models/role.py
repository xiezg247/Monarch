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
    permission = Column(JSON, nullable=False, default=[], comment="角色菜单权限")
    is_admin = Column(Boolean(), nullable=False, default=False, comment="是否管理员")

    users = relationship(
        "User",
        secondary="user_role",
        primaryjoin="Role.id==UserRole.role_id",
        secondaryjoin="User.id==UserRole.user_id",
    )

    @classmethod
    def get_by_id_and_company(cls, id, company_id):
        return cls.query.filter_by(id=id, company_id=company_id).first()

    @classmethod
    def get_by_name_and_company(cls, name, company_id, exclude_id=None):
        query = cls.query.filter_by(name=name, company_id=company_id)
        if exclude_id:
            query = query.filter(cls.id != exclude_id)
        return query.first()

    @classmethod
    def get_roles_by_ids(cls, role_ids):
        roles = []
        if role_ids:
            roles = cls.query.filter(cls.id.in_(role_ids)).all()
        return roles
