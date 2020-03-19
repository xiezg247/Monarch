from monarch.corelibs.store import db
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
    remark = Column(String(128), nullable=True, default=None, comment="备注")
    route_name = Column(String(128), nullable=False, default="/", comment="路由")

    @staticmethod
    def permission_list_to_tree(permission_list):
        nodes = {}
        for i in permission_list:
            id, obj = (i['permission_id'], i)
            nodes[id] = obj

        forest = []
        for i in permission_list:
            id, parent_id, obj = (i['permission_id'], i["parent_id"], i)
            node = nodes[id]

            if parent_id in ["", "0"]:
                forest.append(node)
            else:
                parent = nodes[parent_id]
                if 'children' not in parent:
                    parent['children'] = []
                parent['children'].append(node)
        return forest[0] if forest else {}

    @classmethod
    def gets_by_app_id(cls, app_id, deleted=False):
        return cls.query.filter(cls.app_id == app_id, cls.deleted == deleted).all()

    @classmethod
    def hard_delete_by_app_id(cls, app_id, deleted=False):
        db.session.query(cls).filter(
            cls.app_id == app_id,
            cls.deleted == deleted
        ).delete(synchronize_session=False)
        db.session.commit()
