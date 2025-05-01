import enum
import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Numeric,
    ForeignKey,
    DateTime,
    Enum,
    create_engine,
    func,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserRoleEnum(enum.Enum):
    SUPPLIER = "SUPPLIER"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)  # Consider storing hashed passwords
    email = Column(String(100), nullable=False, unique=True)
    role = Column(Enum(UserRoleEnum), nullable=False)

    # Relationships
    components = relationship("Component", back_populates="user")
    sales = relationship("Sale", back_populates="user")


class Component(Base):
    __tablename__ = "components"

    component_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    # Relationships
    user = relationship("User", back_populates="components")
    sales = relationship("Sale", back_populates="component")


class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True)
    component_id = Column(
        Integer, ForeignKey("components.component_id"), nullable=False
    )
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    sale_date = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User", back_populates="sales")
    component = relationship("Component", back_populates="sales")


# Example of engine creation (usually done elsewhere, e.g., in db.py)
# engine = create_engine('postgresql+psycopg2://user:password@host:port/database')
# Base.metadata.create_all(engine)
