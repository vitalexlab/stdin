from sqlalchemy.orm import Session

from .database import ContractDBModel, ProjectDBModel


class CRUDManager:
    """Common manager to create both Contract and Project"""

    def __init__(self, db_session: Session):
        self.model_class = None
        self.session = db_session
        self.session_query = self.session.query(self.model_class)

    def get_model_instance(self, instance_name: str):
        if issubclass(self.model_class, ContractDBModel):
            return ContractDBModel(contract_name=instance_name)
        return ProjectDBModel(project_name=instance_name)

    def create(self, name: str):
        orm_instance = self.get_model_instance(name[:200])
        self.session.add(orm_instance)
        self.session.commit()
        return orm_instance

    def get_by_name(self, query_name: str):
        if issubclass(self.model_class, ContractDBModel):
            return self.session_query.filter_by(contract_name=query_name).one()
        return self.session_query.filter_by(project_name=query_name).one()

    def get_all(self):
        return self.session_query.all()

    def change_name(self, old_name: str, new_name: str):
        instance = self.get_by_name(old_name)
        if issubclass(self.model_class, ContractDBModel):
            instance.contract_name = new_name[:200]
        else:
            instance.project_name = new_name[:200]
        self.session.commit()
        return instance

    def remove_by_name(self, query_name: str):
        if issubclass(self.model_class, ContractDBModel):
            record = self.session_query.filter_by(
                contract_name=query_name).one()
        else:
            record = self.session_query.filter_by(
                project_name=query_name).one()
        self.session.delete(record)
        self.session.commit()
        return 1


class ContractCRUDManager(CRUDManager):

    def __init__(self, db_session: Session):
        super().__init__(db_session)
        self.model_class = ContractDBModel
        self.session_query = self.session.query(self.model_class)

    def set_project_by_name(self, contract_name, project_name):
        instance = self.session_query.filter_by(contract_name=contract_name)
        project_record = self.session.query(ProjectDBModel).filter_by(
            project_name=project_name)
        instance.project = project_record
        self.session.commit()
        return instance


class ProjectCRUDManager(CRUDManager):
    def __init__(self, db_session: Session):
        super().__init__(db_session)
        self.model_class = ProjectDBModel
        self.session_query = self.session.query(self.model_class)
