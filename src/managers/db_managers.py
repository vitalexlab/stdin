from datetime import datetime
from typing import Type, Union

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.database import ContractDBModel, ProjectDBModel


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
        orm_instance.created_at = datetime.now()
        self.session.add(orm_instance)
        self.session.commit()
        return orm_instance

    def get_by_name(
            self,
            query_name: str
    ) -> Type[Union[ContractDBModel, ProjectDBModel]]:
        if issubclass(self.model_class, ContractDBModel):
            qs = self.session_query.filter_by(contract_name=query_name).first()
        else:
            qs = self.session_query.filter_by(project_name=query_name).first()
        if not qs:
            raise AttributeError('There is no data with such name')
        return qs

    def get_all(self):
        all_ = self.session_query.all()
        return all_

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

    @property
    def object_name(self):
        if issubclass(self.model_class, ContractDBModel):
            return 'contract'
        return 'project'


class ContractCRUDManager(CRUDManager):

    def __init__(self, db_session: Session):
        super().__init__(db_session)
        self.model_class = ContractDBModel
        self.session_query = self.session.query(self.model_class)

    def approve_by_name(self, contract_name: str):
        instance: Type[ContractDBModel] = self.session_query.filter_by(
            contract_name=contract_name
        ).one()
        if instance.is_active or instance.is_finished:
            raise AttributeError('Contract has already approved')
        elif instance.is_draft:
            instance.sign_at = datetime.now()
            instance.is_draft, instance.is_active = False, True
            self.session.commit()
            self.session.close()
        return instance

    def sign_by_name(self, contract_name: str):
        inst = self.session_query.filter_by(contract_name=contract_name).one()
        inst.sign_at, inst.is_finished = datetime.now(), True
        inst.is_active = False
        self.session.commit()
        self.session.close()
        return inst

    def set_contract_by_name(self, contract_name: str, project_name: str):
        contract_instance: Type[ContractDBModel] = self.session.query(
            ContractDBModel
        ).filter_by(contract_name=contract_name).one()
        if contract_instance.is_draft or contract_instance.is_finished:
            raise AttributeError(
                'Only active contracts could be used to link with projects'
            )
        active_contract_count = self.session.query(
            func.count(ContractDBModel.id_contract)).filter(
            ContractDBModel.is_active == True,
            ContractDBModel.project.has(
                ProjectDBModel.project_name == project_name)
        ).scalar()
        if active_contract_count == 1:
            raise AttributeError(
                "Only one active contract should be in a project"
            )
        project_record = self.session.query(ProjectDBModel).filter_by(
            project_name=project_name).one()
        contract_instance.project = project_record
        print(
            f"Active Contract Count in '{project_name}': {active_contract_count}")
        self.session.commit()
        return contract_instance


class ProjectCRUDManager(CRUDManager):
    def __init__(self, db_session: Session):
        super().__init__(db_session)
        self.model_class = ProjectDBModel
        self.session_query = self.session.query(self.model_class)

    def finish_contract(self, contract_name: str, project_name: str):
        inst = self.session_query.filter_by(project_name=project_name).one()
        for contract in inst.contracts:
            print(contract)
            if contract.contract_name == contract_name:
                contract.is_finished = True
                contract.is_active = False
                self.session.commit()
                self.session.close()
            else:
                raise AttributeError(
                    f"Such contract '{contract_name}'does not related to the "
                    f"project '{project_name}'"
                )
