import click
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.database import ContractDBModel, ProjectDBModel, engine
from src.managers.db_managers import ContractCRUDManager, ProjectCRUDManager
from src.utils import get_dashed


class StrategyBaseManager:

    def _should_finish(self, choice) -> bool:
        if choice is None or choice == '0':
            return True
        else:
            return False

    def _get_action(self, choice, manager):
        try:
            get_old_name_text = "Insert old name: "
            get_new_name_text = "Insert new name: "
            if choice == 1:
                old_name = input(get_old_name_text)
                new_name = input(get_new_name_text)
                action = manager.change_name(
                    old_name=old_name, new_name=new_name
                )
                print(f"Name has changed form the '{old_name}' "
                      f"to the '{new_name}'")
                return action
            elif choice == 2:
                project_name = input("Insert valid project name: ")
                contract_name = input("Insert valid contract name: ")
                action = manager.set_project_by_name(
                    project_name=project_name,
                    contract_name=contract_name
                )
                print(f"The project '{project_name}' was "
                      f"attached to the '{contract_name}'")
                return action
        except AttributeError:
            print(get_dashed())
            print('')
            print(f"There is not a contract or project with such name!"
                  f" Aborting!")
        except NoResultFound:
            print(get_dashed())
            print('')
            print(f"There is not a contract or project with such name!"
                  f" Aborting!")

    def _get_db_session(self):
        return sessionmaker(bind=engine)()

    def _get_manager(self):
        if issubclass(self.model_class, ContractDBModel):
            return ContractCRUDManager
        return ProjectCRUDManager

    def create(self):
        instance_name = input(
            f'Insert the name of a {self.manager.object_name}: '
        )
        try:
            self.manager.create(name=instance_name)
            instance = self.manager.get_by_name(query_name=instance_name)
            print(f"A {self.manager.object_name.capitalize()} with name "
                  f"'{instance_name}' was created")
            return instance
        except IntegrityError:
            print('')
            print(f"The {self.manager.object_name} with the name "
                  f"'{instance_name}' already exists! Aborting!!!")
            print('')

    def get_by_name(self):
        while True:
            instance_name = input(
                f'Insert name of a {self.manager.object_name} or 0 to exit: '
            )
            if self._should_finish(instance_name):
                break
            try:
                instance = self.manager.get_by_name(query_name=instance_name)
                print(instance)
                return instance
            except NoResultFound:
                print('')
                print('Sorry, there is not any objects with such name')
                print('')

    def get_all(self):
        queryset = self.manager.get_all()
        print(queryset)
        return queryset

    def change(self):
        while True:
            contract_request_action = ("Choose 1 to change name or choose"
                                       " 2 to set an existing project. "
                                       "(Type 0 to finish): ")
            change_choice = input(contract_request_action)
            if self._should_finish(contract_request_action):
                break
            elif int(change_choice) == 1 or int(change_choice) == 2:
                if issubclass(self.manager_obj, ContractCRUDManager):

                    return self._get_action(
                        choice=int(change_choice),
                        manager=self.manager
                    )
                else:
                    return self._get_action(choice=1, manager=self.manager)
            else:
                print('Insert a valid option')

    def delete(self):
        inter_str = f'Insert a name of a {self.manager.object_name} to delete: '
        object_name = input(inter_str)
        try:
            self.manager.remove_by_name(query_name=object_name)
            print(f"{self.manager.object_name.capitalize()} with "
                  f"name {object_name} was deleted")
        except NoResultFound:
            print(get_dashed())
            print('')
            print(f"No {self.manager.object_name} was found to delete")

    def _run_action_by_choice(self, choice: int):
        choices_actions = {
            '1': self.create,
            '2': self.get_by_name,
            '3': self.get_all,
            '4': self.change,
            '5': self.delete,
        }

        action = choices_actions.get(str(choice))
        return action()

    def run(self):
        self.session = self._get_db_session()
        self.manager_obj = self._get_manager()
        self.manager = self.manager_obj(self.session)
        main_action_text = (
            'Please, choose 1 if you want to create a '
            f'{self.manager.object_name}, 2 - to get '
            'an existing one by name, 3 - to get it all, 4 - to update, '
            '5 - to delete. Choose 0 to '
            'finish. Your choice: ')
        print(get_dashed())
        while True:
            try:
                action: int = int(input(main_action_text))
                if action == 0:
                    break
                elif 5 >= action >= 1:
                    self._run_action_by_choice(choice=action)
                    self.session.close()
                    print('Console program session have finished!')
                    print(get_dashed())
                    break
                else:
                    click.echo('Insert a correct answer')
                    continue
            except ValueError:
                click.echo('Insert a correct answer')
                continue


class StrategyContract(StrategyBaseManager):

    def __init__(self):
        self.model_class = ContractDBModel


class StrategyProject(StrategyBaseManager):

    def __init__(self):
        self.model_class = ProjectDBModel
