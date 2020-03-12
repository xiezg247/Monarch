import shortuuid
from datetime import datetime

from sqlalchemy import (Column, Integer, String, DateTime, Boolean)

from monarch.models.base import Base, TimestampMixin
from monarch.utils.model import escape_like
from monarch.exc.consts import (
    CACHE_COMPANY,
)
from monarch.corelibs.mcredis import mc


class Company(Base, TimestampMixin):
    """公司表"""

    __tablename__ = "company"

    Q_TYPE_NAME = "name"
    Q_TYPE_CODE = "code"

    # status
    STATUS_ON = 1  # 启用
    STATUS_OFF = 2  # 禁用

    id = Column(
        Integer(), nullable=False, autoincrement=True, primary_key=True, comment="公司ID",
    )

    code = Column(String(32), nullable=False, comment="公司编码")
    name = Column(String(128), nullable=True, comment="公司名称")
    expired_at = Column(DateTime(), default=datetime.now, comment="到期日期")
    remark = Column(String(255), nullable=True, comment="企业描述")
    logo = Column(String(255), nullable=True, default=None, comment="企业logo")

    @classmethod
    def paginate_company(cls, query_field, keyword):
        q = []
        if keyword:
            if query_field == Company.Q_TYPE_NAME:
                q.append(cls.name.like("%" + escape_like(keyword) + "%"))

            elif query_field == Company.Q_TYPE_CODE:
                q.append(cls.code.like("%" + escape_like(keyword) + "%"))

        return cls.query.filter(*q).order_by(cls.created_at.desc())

    @property
    def email(self):
        user = User.get_admin_role_by_company_id(self.id, is_admin=True)
        return user.account if user else ""

    @classmethod
    def get_by_code(cls, code, deleted=False):
        return cls.query.filter(cls.code == code, cls.deleted == deleted).first()

    def _clean_cache(self):
        mc.delete(CACHE_COMPANY.format(id=self.id))


class CompanyAdminUser(Base, TimestampMixin):
    """公司管理负责人表"""

    __tablename__ = "company_admin_user"

    id = Column(
        Integer(),
        nullable=False,
        autoincrement=True,
        primary_key=True,
        comment="公司管理负责人ID",
    )

    company_id = Column(Integer, nullable=False, comment="公司ID")
    admin_user_id = Column(String(32), nullable=False, default=None, comment="管理负责人ID")


class CompanyApp(Base, TimestampMixin):
    """公司应用"""
    __tablename__ = "company_app"

    # status
    STATUS_ON = 1  # 启用
    STATUS_OFF = 2  # 禁用

    id = Column(
        Integer(),
        nullable=False,
        autoincrement=True,
        primary_key=True,
        comment="公司应用ID",
    )

    company_id = Column(Integer, nullable=False, comment="公司ID")
    app_id = Column(Integer, nullable=False, default=0, comment="应用ID")
    status = Column(Integer, nullable=False, comment="启用状态")
    expired_at = Column(DateTime(), default=datetime.now, comment="到期日期")
    init_status = Column(Boolean, nullable=False, default=False, comment="初始化状态：1 成功 2 失败")

    @classmethod
    def get_by_company_app_id(cls, company_id, app_id, deleted=False):
        return cls.query.filter(
            cls.company_id == company_id,
            cls.app_id == app_id,
            cls.deleted == deleted
        ).first()


class CompanyAppRobot(Base, TimestampMixin):
    """公司机器人配置表"""

    __tablename__ = "company_app_robot"

    id = Column(
        String(32),
        nullable=False,
        primary_key=True,
        default=shortuuid.uuid,
        comment="公司机器人配置ID",
    )

    company_id = Column(Integer, nullable=False, comment="公司ID")
    app_id = Column(Integer, nullable=False, comment="应用ID")
    robot_url = Column(String(255), nullable=False, default=None, comment="机器人地址")
    robot_version = Column(String(128), default=None, comment="机器人版本")
    robot_key = Column(String(128), default=None, comment="机器人对接key")
    # TODO(xzg): 校验robot

    @classmethod
    def get_by_company_app_id(cls, company_id, app_id, deleted=False):
        return cls.query.filter(
            cls.company_id == company_id,
            cls.app_id == app_id,
            cls.deleted == deleted
        ).first()


# 放在最后避免循环引入问题
from monarch.models.user import User
