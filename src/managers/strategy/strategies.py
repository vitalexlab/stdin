from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.database import ContractDBModel, ProjectDBModel
from src.managers.strategy.base_strategy import StrategyBaseManager
from src.utils import get_dashed


class StrategyContract(StrategyBaseManager):

    """A child of a base manager

    Implements custom methods to add functionality:


    """

    def __init__(self):
        self.model_class = ContractDBModel
        self.choices_to_print = [
            "Choose 1 to change name",
            "Choose 2 to activate (to sign) an existing contract",
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
            print(f"The contract '{contract_name}' was signed (activated)")
            return action
        elif choice == 3:
            action = self.manager.sign_by_name(
                contract_name=contract_name
            )
            print(f"The contract '{contract_name}' was finished")
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
            print(f"\n{get_dashed()}\nThere is not a contract or project with "
                  "such name! Aborting!")


class StrategyProject(StrategyBaseManager):

    def __init__(self):
        self.model_class = ProjectDBModel
        self.choices_to_print = [
            "Choose 1 to change name",
            "Choose 2 to finish a contract for the project",
            "Choose 3 to set contract to the project",
            "(Type 0 to finish)",
        ]
        self.menu_input_text = "Your choice: "

    def check_active_contracts(self):
        active_contract_count = self.session.query(
            func.count(ContractDBModel.id_contract)).filter(
            ContractDBModel.is_active == True
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
