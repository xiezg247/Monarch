from monarch.models.base import Base, TimestampMixin
from sqlalchemy import Column, String, Integer


class AppPermission(Base, TimestampMixin):
    """应用菜单表"""

    __tablename__ = "app_permission"

    id = Column(
        Integer(), nullable=False, autoincrement=True, primary_key=True, comment="自增长ID",
    )

    app_id = Column(Integer, nullable=False, default=0, comment="应用ID")

    name = Column(String(32), nullable=False, comment="权限名称")
    parent_id = Column(String(32), nullable=False, default="", comment="上报父级权限ID")
    permission_id = Column(String(32), nullable=False, default="", comment="上报权限ID")
    remark = Column(String(128), nullable=False, comment="备注")
    route_name = Column(String(128), nullable=False, default="/", comment="路由")

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
    def gets_by_app_id(cls, app_id, deleted=False):
        return cls.query.filter(cls.app_id == app_id, cls.deleted == deleted).all()
