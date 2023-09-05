from abc import abstractmethod

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.database import ContractDBModel, ProjectDBModel, engine
from src.managers.db_managers import ContractCRUDManager, ProjectCRUDManager
from src.utils import get_dashed


class StrategyBaseManager:

    """Base manager for ContractStrategy and ProjectStratagy

     It is made to run strategy depended on is it a contract or project.
     CRUD operations are implemented
     """

    def _should_finish(self, choice) -> bool:
        if choice is None or choice == '0':
            return True
        else:
            return False

    @abstractmethod
    def _run_change(self):
        pass

    @abstractmethod
    def _get_action(self, choice, contract_name=None):
        pass

    @abstractmethod
    def _change_status(self, choice: int, contract_name=None):
        pass

    def _run_change_menu(self) -> str:
        for choice in self.choices_to_print:
            print(choice)
        chosen_variant = input(self.menu_input_text)
        return chosen_variant

    def _get_db_session(self):
        return sessionmaker(bind=engine)()

    def _get_manager(self):
        if issubclass(self.model_class, ContractDBModel):
            return ContractCRUDManager
        return ProjectCRUDManager

    def _change_name(self):
        get_old_name_text = "Insert old name: "
        get_new_name_text = "Insert new name: "
        old_name = input(get_old_name_text)
        new_name = input(get_new_name_text)
        action = self.manager.change_name(
            old_name=old_name, new_name=new_name
        )
        print(f"Name has changed form the '{old_name}' "
              f"to the '{new_name}'")
        return action

    def create(self):

        if issubclass(self.model_class, ProjectDBModel):
            if not self.check_active_contracts():
                raise AttributeError(
                    'Should be 1 more active contract to create a project'
                )
        instance_name = input(
            f'Insert the name of a {self.manager.object_name}: '
        )
        try:
            self.manager.create(name=instance_name)
            self.instance = self.manager.get_by_name(query_name=instance_name)
            print(f"A {self.manager.object_name.capitalize()} with name "
                  f"'{instance_name}' was created")
            self.session.refresh(self.instance)
            return self.instance
        except IntegrityError:
            print(f"\nThe {self.manager.object_name} with the name "
                  f"'{instance_name}' already exists! Aborting!!!\n")

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
                print('\nSorry, there is not any objects '
                      'with such name.Try again.\n')

    def get_all(self):
        queryset = self.manager.get_all()
        print(queryset)
        return queryset

    def change(self):
        while True:
            run_status, data = self._run_change()
            if run_status is None:
                print('Insert a valid option')
                continue
            elif not run_status:
                break
            else:
                return data

    def delete(self):
        inter_str = (f'Insert a name of a {self.manager.object_name} '
                     f'to delete: ')
        object_name = input(inter_str)
        try:
            self.manager.remove_by_name(query_name=object_name)
            print(f"\n{self.manager.object_name.capitalize()} with "
                  f"name {object_name} was deleted\n")
        except NoResultFound:
            print(get_dashed())
            print(f"\nNo {self.manager.object_name} was found to delete.\n")

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
            'an existing one by name, 3 - to get it all, 4 - to change, '
            '5 - to delete. Choose 0 to finish. Your choice: ')
        print(get_dashed())
        while True:
            try:
                action: int = int(input(main_action_text))
                if action == 0:
                    break
                elif 5 >= action >= 1:
                    self._run_action_by_choice(choice=action)
                    self.session.close()
                    print(f'Console program session '
                          f'have finished!\n{get_dashed()}')
                    break
                else:
                    print('Insert a correct answer')
                    continue
            except ValueError:
                print('Insert a correct answer')
                continue
            except AttributeError as ae:
                print(ae)
                break


class StrategyContract(StrategyBaseManager):

    """A child of a base manager

    Implements custom methods to add functionality:


    """

    def __init__(self):
        self.model_class = ContractDBModel
        self.choices_to_print = [
            "Choose 1 to change name",
            "Choose 2 to approve an existing contract",
            "Choose 3 to finish an existing contract",
            "Choose 4 to set a project to the contract",
            "(Type 0 to finish)",
        ]
        self.menu_input_text = "Your choice: "

    def _run_change(self):
        change_choice = self._run_change_menu()
        if self._should_finish(change_choice):
            return False, None
        elif int(change_choice) in [1, 2, 3, 4]:
            return True, self._get_action(choice=int(change_choice))
        else:
            return None, None

    def _change_status(self, choice: int, contract_name=None):
        if contract_name is None:
            contract_name = input("Insert valid contract name: ")
        if choice == 2:
            action = self.manager.approve_by_name(
                contract_name=contract_name
            )
            print(f"The contract '{contract_name}' was approved")
            return action
        elif choice == 3:
            action = self.manager.sign_by_name(
                contract_name=contract_name
            )
            print(f"The contract '{contract_name}' was signed")
            return action
        elif choice == 4:
            project_name = input("Insert valid project name: ")
            try:
                action = self.manager.set_contract_by_name(
                        contract_name=contract_name,
                        project_name=project_name
                    )
                print(f"The contract '{contract_name}' was set to"
                      f" the project'{project_name}'")
                return action
            except IntegrityError:
                print('A contract could be set to only one project')

    def _get_action(self, choice, contract_name=None):
        try:
            if choice == 1:
                action = self._change_name()
            elif choice > 1:
                action = self._change_status(choice=choice, contract_name=None)
            return action
        except AttributeError as ae:
            print(f"\n{get_dashed()}\n{ae}\nAborting!")
        except NoResultFound:
            print("\n{get_dashed()}\nThere is not a contract or project with "
                  "such name! Aborting!")


class StrategyProject(StrategyBaseManager):

    def __init__(self):
        self.model_class = ProjectDBModel
        self.choices_to_print = [
            "Choose 1 to change name",
            "Choose 2 to finish a contract for the project",
            "Choose 3 to set contract to the project"
            "(Type 0 to finish)",
        ]
        self.menu_input_text = "Your choice: "

    def check_active_contracts(self):
        active_contract_count = self.session.query(
            func.count(ContractDBModel.id_contract)).filter(
            ContractDBModel.is_active is True
        ).scalar()
        if active_contract_count >= 1:
            return True
        return False

    def _run_change(self):
        change_choice = self._run_change_menu()
        if self._should_finish(change_choice):
            return False, None
        elif int(change_choice) in [1, 2, 3]:
            return True, self._get_action(choice=int(change_choice))
        else:
            return None, None

    def _change_status(self, choice: int, contract_name=None):
        if contract_name is None:
            contract_name = input("Insert valid contract name: ")
        project_name = input("Insert valid project name: ")
        if choice == 3:
            action = self.manager.set_contract_by_name(
                contract_name=contract_name,
                project_name=project_name
            )
            print(f"The contract '{contract_name}' was set to"
                  f" the project'{project_name}'")
        if choice == 2:
            action = self.manager.finish_contract(
                contract_name=contract_name,
                project_name=project_name
            )
            print(f"The contract '{contract_name}' was finished for "
                  f"the project '{project_name}'")
        return action

    def _get_action(self, choice, contract_name=None):
        try:
            if choice == 1:
                action = self._change_name()
            elif choice == 2 or choice == 3:
                action = self._change_status(choice=choice)
            return action
        except AttributeError as ae:
            print(f"\n{get_dashed()}\n{ae}\nAborting!")
        except NoResultFound:
            print("such name!\nThere is not a contract or project with "
                  "such name! Aborting!")
