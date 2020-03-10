import shortuuid
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy import (Column, Integer, String, JSON, DateTime, UniqueConstraint)

from monarch.corelibs.cache_decorator import cache
from monarch.models.base import Base, TimestampMixin, model_cache
from monarch.utils.model import escape_like
from monarch.exc.consts import (
    CACHE_WEEK,
    CACHE_COMPANY_ALL,
    CACHE_COMPANY,
)
from monarch.utils.api import parse_pagination
from monarch.corelibs.store import db
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
    status = Column(Integer, nullable=False, default=0, comment="开启状态")
    logo = Column(String(255), nullable=True, default=None, comment="企业logo")

    @classmethod
    @model_cache(CACHE_COMPANY, CACHE_WEEK)
    def get(cls, id, exclude_deleted=True):
        return super().get(id=id, exclude_deleted=exclude_deleted)

    @classmethod
    def get_company_by_code(cls, code):
        return cls.query.filter_by(code=code).first()

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
        user = User.get_by_company_id(self.id, is_admin=True)
        return user.account if user else ""

    @classmethod
    def create_company_and_init_settings(cls, company_data, permission_data):
        company = cls.create(
            code=shortuuid.uuid(),
            name=company_data.get("name"),
            expired_at=company_data.get("expired_at"),
            status=company_data.get("status"),
            remark=company_data.get("remark"),
        )

        # 公司菜单权限
        db.session.add(CompanyMenu.create(
            company_id=company.id,
            permission=permission_data,
            _commit=False
        ))

        # 公司对应的智言运营
        db.session.add(CompanyAdminUser.create(
            company_id=company.id,
            admin_user_id=company_data.get("admin_user_id"),
            _commit=False
        ))

        # 公司管理员
        db.session.add(User.create(
            id=shortuuid.uuid(),
            company_id=company.id,
            account=company_data.get("email"),
            password=company_data.get("password"),
            username="admin",
            nickname="admin",
            is_admin=True,
            enabled=True,
            _commit=False
        ))

        # 统一提交 错误回滚 回滚后需要删除已创建的公司信息
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            company.delete(_hard=True)
            raise
        return company

    @classmethod
    @cache(CACHE_COMPANY_ALL, CACHE_WEEK)
    def all(cls, exclude_deleted=True):
        return super().all(exclude_deleted=exclude_deleted)

    def _clean_cache(self):
        mc.delete(CACHE_COMPANY.format(id=self.id))
        mc.delete(CACHE_COMPANY_ALL)


class CompanyMenu(Base, TimestampMixin):
    """公司菜单表"""

    __tablename__ = "company_menu"

    id = Column(
        Integer(),
        nullable=False,
        autoincrement=True,
        primary_key=True,
        comment="公司菜单ID",
    )

    company_id = Column(Integer, nullable=False, comment="公司ID")
    permission = Column(JSON, nullable=False, default=[], comment="公司菜单权限")

    @classmethod
    def get_by_company_id(cls, company_id, deleted=False):
        return cls.query.filter(
            cls.company_id == company_id, cls.deleted == deleted
        ).first()

    @classmethod
    def get_menus_by_company_id(cls, company_id, deleted=False):
        menu = cls.get_by_company_id(company_id)
        menus = Menu.get_menus_by_ids(menu.permission, deleted)
        return menus


class CompanyRobot(Base, TimestampMixin):
    """公司机器人配置表"""

    __tablename__ = "company_robot"
    __table_args__ = (UniqueConstraint("robot_url", "robot_key"), UniqueConstraint("company_id", "name"))

    id = Column(
        String(32),
        nullable=False,
        primary_key=True,
        default=shortuuid.uuid,
        comment="公司机器人配置ID",
    )

    company_id = Column(Integer, nullable=False, comment="公司ID")
    name = Column(String(128), nullable=False, default=None, comment="机器人名称")
    robot_url = Column(String(255), nullable=False, default=None, comment="机器人地址")
    robot_version = Column(String(128), default=None, comment="机器人版本")
    robot_key = Column(String(128), default=None, comment="机器人对接key")
    status = Column(Integer, nullable=False, default=0, comment="启用(绑定)状态")

    @classmethod
    def get_list_by_company_id(cls, company_id):
        query = cls.query_by_exist().filter_by(company_id=company_id).order_by(cls.created_at.desc())
        return parse_pagination(query)

    @classmethod
    def get_by_company_id_and_name(cls, company_id, name):
        return cls.query_by_exist().filter_by(company_id=company_id, name=name).first()

    @classmethod
    def get_by_robot_url_and_robot_key(cls, robot_url, robot_key):
        return cls.query_by_exist().filter_by(robot_url=robot_url, robot_key=robot_key).first()


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


# 放在最后避免循环引入问题
from monarch.models.menu import Menu
from monarch.models.user import User
