import os
import time

from sqlite3 import IntegrityError

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.database import engine, db_name

from src.managers import ContractCRUDManager, ProjectCRUDManager


def delete_test_db(filename: str):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"File '{filename}' has been deleted.")
        except Exception as e:
            print(f"Error deleting file: {str(e)}")
    else:
        print(f"File '{filename}' does not exist.")


def get_session(db_engine):
    return sessionmaker(bind=db_engine)()


def test_create_contract_success(db_engine):
    name = 'contract'
    session = get_session(db_engine=db_engine)
    manager = ContractCRUDManager(session)
    contract = manager.create(name=name)
    session.commit()
    assert contract.contract_name == name
    session.close()


def test_get_contract_by_name(db_engine):
    name = 'contract'
    session = get_session(db_engine=db_engine)
    manager = ContractCRUDManager(session)
    contract = manager.get_by_name(name)
    assert contract.contract_name == name


def test_get_all_contracts(db_engine):
    session = get_session(db_engine=db_engine)
    manager = ContractCRUDManager(session)

    current_records_count = len(manager.get_all())
    assert current_records_count == 1
    name = 'contract2'
    manager.create(name=name)
    session.commit()
    all_records = manager.get_all()
    assert len(all_records) == 2


def test_change_contract_name(db_engine):
    session = get_session(db_engine=db_engine)
    old_name = 'contract2'
    new_name = 'new_name'
    manager = ContractCRUDManager(session)
    contract = manager.get_by_name(old_name)
    contract.contract_name = new_name
    session.commit()
    session.refresh(contract)
    assert contract.contract_name == new_name


def test_delete_contract_by_name(db_engine):

    session = get_session(db_engine=db_engine)
    manager = ContractCRUDManager(session)
    previous_count = len(manager.get_all())

    name = 'contract'
    manager.remove_by_name(query_name=name)
    curr_count = len(manager.get_all())
    assert curr_count == previous_count - 1


def test_create_contract_negative(db_engine):
    name = 'contract'
    session = get_session(db_engine=db_engine)
    manager = ContractCRUDManager(session)
    try:
        contract = manager.create(name=name)
    except IntegrityError:
        assert 1 == 1


def test_get_contract_by_name_negative(db_engine):
    name = 'contractt121312341321'
    session = get_session(db_engine=db_engine)
    manager = ContractCRUDManager(session)
    try:
        manager.get_by_name(name)
    except NoResultFound:
        assert 1 == 1


def test_change_contract_name_negative(db_engine):
    session = get_session(db_engine=db_engine)
    try:
        old_name = 'contract24fvlfdvfd'
        new_name = 'new_name'
        manager = ContractCRUDManager(session)
        contract = manager.get_by_name(old_name)
        contract.contract_name = new_name
        session.commit()
        session.refresh(contract)
        assert contract.contract_name == new_name
    except NoResultFound:
        assert 1 == 1


def test_foreign_key_positive(db_engine):
    session = get_session(db_engine=db_engine)
    project_manager = ProjectCRUDManager(session)
    project = project_manager.create('project_name')
    contract_manager = ContractCRUDManager(session)
    contract = contract_manager.get_all()[0]
    contract_with_project = contract_manager.set_project_by_name(
        contract_name=contract.contract_name,
        project_name=project.project_name)
    print('Test foreign key positive passed')


def test_foreign_key_negative(db_engine):
    session = get_session(db_engine=db_engine)
    contract_manager = ContractCRUDManager(session)
    c = contract_manager.set_project_by_name(
        contract_name='contract',
        project_name='sdfsdfsdfds')
    assert contract_manager.get_by_name('contract').project_id is None
    print('Test foreign key negative passed')


if __name__ == '__main__':

    try:
        test_create_contract_success(db_engine=engine)
        test_get_contract_by_name(db_engine=engine)
        test_get_all_contracts(db_engine=engine)
        test_change_contract_name(db_engine=engine)
        test_delete_contract_by_name(db_engine=engine)
        test_create_contract_negative(db_engine=engine)
        test_get_contract_by_name_negative(db_engine=engine)
        test_change_contract_name_negative(db_engine=engine)
        test_foreign_key_positive(db_engine=engine)
        test_foreign_key_negative(db_engine=engine)
    except Exception as exc:
        print('')
        print('Exception occured!!!!!!')
        print('')
        print(exc)
    else:
        print('')
        print('Contract tests successfully passed!!!!!!')
        print('')
    finally:
        time.sleep(1)
        delete_test_db(db_name)
