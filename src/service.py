from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, NoResultFound

from database import engine
from src.manager import ProjectCRUDManager

if __name__ == '__main__':
    name = 'new_proj131'
    session = sessionmaker(bind=engine)()
    try:
        proj_instance = ProjectCRUDManager(session)
        # proj_orm_create = proj_instance.create(name=name)
        # print(proj_orm_create.project_name)
        # session.refresh(proj_orm_create)
        # proj_orm_get_by_name = proj_instance.get_by_name(query_name=name)
        # print(proj_orm_get_by_name.project_name)
        # proj_orm_create = proj_instance.create(name='sfvsfdvsd')
        proj_orm_get_all = proj_instance.get_all()
        print([x.id_project for x in proj_orm_get_all])
        # proj_orm_update = proj_instance.change_name(old_name=name, new_name='124')
        # print(proj_orm_update.project_name)
        # proj_orm_delete = proj_instance.remove_by_name(query_name='124')
        # print(proj_orm_delete)
    except IntegrityError:
        print('Such contract already exists')

    # except Exception as e:
    #     print(f'Error accessing contract attributes: {str(e)}')
    finally:
        session.close()
