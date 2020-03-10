from werkzeug.security import generate_password_hash, check_password_hash

from monarch.models.base import Base, TimestampMixin
from sqlalchemy import Column, String


class AdminUser(Base, TimestampMixin):
    """管理员表"""
    __tablename__ = "admin_user"

    Q_TYPE_ACCOUNT = "account"

    id = Column(
        String(32),
        nullable=False,
        primary_key=True,
        comment="管理员ID",
    )

    account = Column(String(32), nullable=False, comment="账号")
    # password 为 表字段 的名字，实则为了解决赋值时直接将 password 赋值给模型（password字段不存在，所以无法赋值）,为了加密
    _password = Column("password", String(128), nullable=False, default=None, comment="密码")

    @property
    def password(self):
        '''
        getter 函数
        读取 password 字段
        :return:
        '''
        return self._password

    @password.setter
    def password(self, raw):
        '''
         setter 函数
        解决明文存储 password 问题
        设置 password 字段
        :param raw:
        :return:
        '''
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
