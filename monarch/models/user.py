from sqlalchemy import Index

from monarch.models.base import Base, TimestampMixin

from monarch.corelibs.store import db
from monarch.corelibs.mcredis import mc
from monarch.corelibs.cache_decorator import cache

from monarch.exc.consts import CACHE_DAY
from monarch.utils.model import escape_like


class User(Base, TimestampMixin):
    """用户类"""

    __tablename__ = "user"

    __table_args__ = (
        # UniqueConstraint('unionid', 'deleted'， name='idx_unionid_deleted'),
        # 唯一索引/唯一性约束
        Index("idx_unionid_deleted", "unionid", "deleted", unique=True),
        # 普通索引
        Index("idx_uid", "uid"),
    )

    # query type
    Q_TYPE_PHONE = "phone"
    Q_TYPE_USERNAME = "username"

    # user type
    USER_TYPE_ANONYMOUS = 1  # 匿名用户
    USER_TYPE_WECHAT = 2  # 微信用户
    USER_TYPE_NORMAL = 3  # 普通用户

    id = db.Column(
        db.Integer(),
        nullable=False,
        autoincrement=True,
        primary_key=True,
        comment="自增长ID",
    )
    uid = db.Column(db.String(50), nullable=False, comment="用户唯一标识")
    openid = db.Column(db.String(50), comment="用户微信openid")
    unionid = db.Column(db.String(50), nullable=False, comment="用户微信unionid")
    username = db.Column(db.String(100), comment="用户姓名")
    avatar = db.Column(db.String(160), comment="用户头像")
    phone = db.Column(db.String(11), comment="用户手机号码")
    qrcode = db.Column(db.String(160), comment="用户微信二维码")
    source_type = db.Column(db.Integer, comment="用户角色 1:匿名用户 2:微信用户 3:普通用户")

    @classmethod
    def get_all(cls):
        return cls.query.filter(cls.deleted == 0).order_by(cls.created_at.desc())

    @classmethod
    @cache("mc:user:uid:{uid}", CACHE_DAY)
    def get_by_uid(cls, uid):
        return cls.query.filter(cls.uid == uid).first()

    @classmethod
    def paginate_user(cls, query_field, keyword, source_type):
        q = []
        if keyword:
            if query_field == User.Q_TYPE_PHONE:
                q.append(cls.phone.like("%" + escape_like(keyword) + "%"))

            elif query_field == User.Q_TYPE_USERNAME:
                q.append(cls.username.like("%" + escape_like(keyword) + "%"))

        if source_type:
            q.append(cls.source_type == source_type)
        else:
            q.append(
                cls.source_type.in_(
                    [
                        User.USER_TYPE_ANONYMOUS,
                        User.USER_TYPE_WECHAT,
                        User.USER_TYPE_NORMAL,
                    ]
                )
            )

        return cls.query.filter(*q).order_by(cls.created.desc())

    def _clean_cache(self):
        mc.delete("mc:user:uid:{}".format(self.uid))
