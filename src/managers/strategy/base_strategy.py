from abc import abstractmethod

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
