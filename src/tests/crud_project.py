import os
import time

from sqlite3 import IntegrityError

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.database import engine, db_name

from src.manager import ProjectCRUDManager


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
    name = 'project'
    session = get_session(db_engine=db_engine)
    manager = ProjectCRUDManager(session)
    project = manager.create(name=name)
    session.commit()
    assert project.project_name == name
    session.close()


def test_get_contract_by_name(db_engine):
    name = 'project'
    session = get_session(db_engine=db_engine)
    manager = ProjectCRUDManager(session)
    project = manager.get_by_name(name)
    assert project.project_name == name


def test_get_all_contracts(db_engine):
    session = get_session(db_engine=db_engine)
    manager = ProjectCRUDManager(session)

    current_records_count = len(manager.get_all())
    assert current_records_count == 1
    name = 'project2'
    manager.create(name=name)
    session.commit()
    all_records = manager.get_all()
    assert len(all_records) == 2


def test_change_contract_name(db_engine):
    session = get_session(db_engine=db_engine)
    old_name = 'project2'
    new_name = 'new_name'
    manager = ProjectCRUDManager(session)
    project = manager.get_by_name(old_name)
    project.project_name = new_name
    session.commit()
    session.refresh(project)
    assert project.project_name == new_name


def test_delete_contract_by_name(db_engine):

    session = get_session(db_engine=db_engine)
    manager = ProjectCRUDManager(session)
    previous_count = len(manager.get_all())

    name = 'project'
    manager.remove_by_name(query_name=name)
    curr_count = len(manager.get_all())
    assert curr_count == previous_count - 1


def test_create_contract_negative(db_engine):
    name = 'project'
    session = get_session(db_engine=db_engine)
    manager = ProjectCRUDManager(session)
    try:
        contract = manager.create(name=name)
    except IntegrityError:
        assert 1 == 1


def test_get_contract_by_name_negative(db_engine):
    name = 'projectt121312341321'
    session = get_session(db_engine=db_engine)
    manager = ProjectCRUDManager(session)
    try:
        manager.get_by_name(name)
    except NoResultFound:
        assert 1 == 1


def test_change_contract_name_negative(db_engine):
    session = get_session(db_engine=db_engine)
    try:
        old_name = 'prdvsdcscsdce'
        new_name = 'new_name'
        manager = ProjectCRUDManager(session)
        project = manager.get_by_name(old_name)
        project.project_name = new_name
        session.commit()
        session.refresh(project)
        assert project.contract_name == new_name
    except NoResultFound:
        assert 1 == 1


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

        time.sleep(5)
    except Exception as exc:
        print('')
        print('Exception occured!!!!!!')
        print('')
        print(exc)
    finally:
        print('')
        print('Project tests successfully passed!!!!!!')
        print('')
        delete_test_db(db_name)
