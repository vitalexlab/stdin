import click
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.database import ContractDBModel, ProjectDBModel, engine
from src.managers.db_managers import ContractCRUDManager, ProjectCRUDManager
from src.utils import get_dashed


class StrategyBaseManager:

    def _get_action(self, choice, manager):
        get_old_name_text = "Insert old name: "
        get_new_name_text = "Insert new name: "
        if choice == 1:
            old_name = input(get_old_name_text)
            new_name = input(get_new_name_text)
            return manager.change_name(old_name=old_name, new_name=new_name)
        elif choice == 2:
            project_name = input("Insert valid project name: ")
            contract_name = input("Insert valid contract name: ")
            return manager.set_project_by_name(
                project_name=project_name,
                contract_name=contract_name
            )

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
            if not bool(instance_name) or instance_name == '0':
                break
            try:
                instance = self.manager.get_by_name(query_name=instance_name)
                return instance.get_name()
            except NoResultFound:
                print('')
                print('Sorry, there is not any objects with such name')
                print('')

    def get_all(self):
        return self.manager.get_all()

    def change(self):
        contract_request_action = ("Choose 1 to change name or choose 2 to "
                                   "set an existing project")
        if issubclass(self.manager_obj, ContractCRUDManager):
            contr_change_choice = input(contract_request_action)
            return self._get_action(
                choice=contr_change_choice,
                manager=self.manager
            )
        else:
            return self._get_action(choice=1, manager=self.manager)

    def delete(self):
        inter_str = f'Insert a name of a {self.manager.object_name} to delete: '
        object_name = input(inter_str)
        return self.manager.remove_by_name(query_name=object_name)

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


class StrategyContract(StrategyBaseManager):

    def __init__(self):
        self.model_class = ContractDBModel


class StrategyProject(StrategyBaseManager):

    def __init__(self):
        self.model_class = ProjectDBModel
