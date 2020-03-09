"""create user table

Revision ID: f7531bc7da19
Revises:
Create Date: 2019-04-09 01:23:55.668648

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'f7531bc7da19'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
                    sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.now, comment='创建时间'),
                    sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.now,
                              onupdate=datetime.now, comment='更新时间'),
                    sa.Column('deleted', sa.Boolean(), nullable=False, default=False, comment='是否删除'),

                    sa.Column('uid', sa.String(50), nullable=False, comment='用户唯一标识'),
                    sa.Column('openid', sa.String(50), comment='用户微信openid'),
                    sa.Column('unionid', sa.String(50), nullable=False, comment='用户微信unionid'),
                    sa.Column('username', sa.String(100), comment='用户姓名'),
                    sa.Column('avatar', sa.String(160), comment='用户头像'),
                    sa.Column('company', sa.String(50), comment='用户所属公司'),
                    sa.Column('position', sa.String(50), comment='用户职位'),
                    sa.Column('phone', sa.String(11), comment='用户手机号码'),
                    sa.Column('qrcode', sa.String(160), comment='用户微信二维码'),
                    sa.Column('source_type', sa.Integer, comment='用户角色 1:匿名用户 2:微信用户 3:普通用户'),
                    sa.Index('idx_unionid_deleted', 'unionid', 'deleted', unique=True),
                    sa.Index('idx_uid', 'uid'),
                    )


def downgrade():
    op.drop_table('user')
