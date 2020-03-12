from monarch.models.base import Base, TimestampMixin
from sqlalchemy import Column, String, Integer


class Menu(Base, TimestampMixin):
    """菜单表"""

    __tablename__ = "menu"

    id = Column(
        Integer(), nullable=False, autoincrement=True, primary_key=True, comment="菜单ID",
    )

    name = Column(String(32), nullable=False, comment="菜单名称")
    parent_id = Column(Integer, nullable=False, default=0, comment="父级菜单ID")

    @classmethod
    def get_by_name_and_parent_id(cls, name, parent_id):
        return cls.query.filter(cls.name == name, cls.parent_id == parent_id).first()
