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

    @staticmethod
    def menu_list_to_tree(menu_list):
        tree = {0: {"id": 0, "parent_id": 0, "name": "总后台", "children": []}}

        for menu in menu_list:
            tree.setdefault(menu["parent_id"], {"children": []})
            tree.setdefault(menu["id"], {"children": []})
            tree[menu["id"]].update(menu)
            tree[menu["parent_id"]]["children"].append(tree[menu["id"]])

        return tree[0]

    @classmethod
    def get_menus_by_ids(cls, menu_ids, deleted=False):
        menus = []
        if menu_ids:
            menus = cls.query.filter(cls.id.in_(menu_ids), cls.deleted == deleted).all()
        return menus

    @classmethod
    def get_by_name_and_parent_id(cls, name, parent_id):
        return cls.query.filter(cls.name == name, cls.parent_id == parent_id).first()
