from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

db_name = 'orders.db'
connection = f'sqlite:///{db_name}'
engine = create_engine(connection, echo=True)


class ContractDBModel(Base):
    __tablename__ = 'order_contract'

    id_contract = Column('id_contract', Integer, primary_key=True,
                         autoincrement=True)
    contract_name = Column('contract_name', String(200), unique=True)
    created_at = Column('created_at', DateTime, nullable=True)
    sign_at = Column('sign_at', DateTime, nullable=True)
    is_draft = Column('is_draft', Boolean, nullable=False, default=True)
    is_active = Column('is_active', Boolean, nullable=False, default=False)
    is_approved = Column('is_approved', Boolean, nullable=False, default=False)
    project_id = Column('project_id', Integer,
                        ForeignKey('order_project.id_project'))


class ProjectDBModel(Base):
    __tablename__ = 'order_project'

    id_project = Column('id_project', Integer, primary_key=True,
                        autoincrement=True)
    project_name = Column('project_name', String(200), unique=True)
    created_at = Column('created_at', DateTime, nullable=True)
    contracts = relationship("ContractDBModel", backref="project",
                             uselist=True)


Base.metadata.create_all(engine)
