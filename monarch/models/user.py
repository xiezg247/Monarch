import shortuuid
from sqlalchemy import Index, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from monarch.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """客服表"""

    __tablename__ = "user"

    __table_args__ = (
        # 唯一索引/唯一性约束
        Index("idx_account_deleted", "account", "deleted", unique=True),
        # 普通索引
        Index("idx_company_id", "company_id"),
    )

    id = Column(
        String(32),
        nullable=False,
        primary_key=True,
        default=shortuuid.uuid,
        comment="客服ID",
    )
    company_id = Column(Integer, nullable=False, comment="公司ID")
    account = Column(String(32), nullable=False, comment="账号")
    username = Column(String(32), nullable=False, comment="用户姓名")
    nickname = Column(String(64), nullable=True, comment="用户昵称")
    avatar = Column(String(255), nullable=True, default=None, comment="用户头像")
    mobile = Column(String(16), nullable=True, comment="手机号码")
    enabled = Column(Boolean(), nullable=False, default=False, comment="是否禁止")

    # password 为 表字段 的名字，实则为了解决赋值时直接将 password 赋值给模型（password字段不存在，所以无法赋值）,为了加密
    _password = Column(
        "password", String(128), nullable=False, default=None, comment="密码"
    )

    roles = relationship(
        "Role",
        secondary="user_role",
        primaryjoin="User.id==UserRole.user_id",
        secondaryjoin="Role.id==UserRole.role_id",
    )

    company = relationship(
        "Company",
        uselist=False,
        foreign_keys=company_id,
        primaryjoin="User.company_id==Company.id",
    )

    @property
    def password(self):
        """
        getter 函数
        读取 password 字段
        :return:
        """
        return self._password

    @password.setter
    def password(self, raw):
        """
         setter 函数
        解决明文存储 password 问题
        设置 password 字段
        :param raw:
        :return:
        """
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    def reset_password(self, new_password):
        self._password = generate_password_hash(new_password)
        self.save()
        return True


class UserRole(Base, TimestampMixin):
    """客服角色表"""

    __tablename__ = "user_role"

    id = Column(
        Integer(),
        nullable=False,
        autoincrement=True,
        primary_key=True,
        comment="客服角色ID",
    )

    user_id = Column(String(32), nullable=False, comment="客服ID")
    role_id = Column(Integer, nullable=False, comment="角色ID")
