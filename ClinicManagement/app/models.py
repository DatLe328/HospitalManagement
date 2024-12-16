from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from app import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin


class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1679134375/ckvdo90ltnfns77zf1xb.jpg')
    user_role = Column(Enum(UserRole), default=UserRole.USER)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        import hashlib
        u = User(name='admin', username='admin',
                 password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRole.ADMIN)
        db.session.add(u)
        db.session.commit()