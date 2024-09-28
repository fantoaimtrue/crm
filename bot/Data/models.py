from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Profile(Base):
    __tablename__ = 'UserProfile_profile'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    email = Column(String, nullable=True)
    wb_token = Column(String, nullable=True)
    ozon_token = Column(String, nullable=True)
    ozon_client_id = Column(Integer, nullable=True, default=0)
    tg_username = Column(String, nullable=True)

    def __repr__(self):
        return f"<Profile(email={self.email})>"
