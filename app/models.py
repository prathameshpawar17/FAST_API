from sqlalchemy import Column, Integer, String
from passlib.context import CryptContext
from .database import Base

 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.hashed_password)

    @staticmethod
    def hash_password(password: str):
        return pwd_context.hash(password)
