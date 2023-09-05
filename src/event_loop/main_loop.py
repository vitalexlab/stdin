from src.managers.strategy.strategies import StrategyContract, StrategyProject
from src.utils import get_dashed

STRATEGY_SELECTION = ('Please, chose 1 for running a work with Contracts, '
                      'or 2 to start with Projects, or 0 to finish: ')


class MainLoop:
    """Main event loop for the all actions"""

    @staticmethod
    def _get_manager_by_choice(choice: int):
        """Returns manager dependened on the choice"""

        return StrategyContract if choice == 1 else StrategyProject

    def _choose_strategy(self):
        negative_answer = ('Insert a correct answer, please enter an integer '
                           'from 0 to 2')
        while True:
            try:
                choice: int = int(input(STRATEGY_SELECTION))
                print(f"{get_dashed()}\n{get_dashed()}")
                if choice == 0:
                    break
                elif choice == 1 or choice == 2:
                    manager = self._get_manager_by_choice(choice=choice)
                    return manager()
                else:
                    print(negative_answer)
                    continue
            except ValueError:
                print(negative_answer)
                continue

    @staticmethod
    def _greeting():
        print(f"{get_dashed()}\n\nHello from the "
              f"console program!\n\n{get_dashed()}")

    def run(self):
        try:
            self._greeting()
            strategy = self._choose_strategy()
            strategy.run()
        except AttributeError:
            pass
