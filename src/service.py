from sqlalchemy.orm import sessionmaker

from database import engine, ProjectDBModel
from src.managers import ProjectCRUDManager, ContractCRUDManager

if __name__ == '__main__':
    name = 'new_proj131'
    session = sessionmaker(bind=engine)()
    contract_manager = ContractCRUDManager(session)
    contract = contract_manager.create(name='123456')
    proj_manager = ProjectCRUDManager(session)
    proj = session.query(ProjectDBModel).filter_by(project_name='1234ed').count()
