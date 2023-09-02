from abc import ABC, abstractmethod

import click
from src.stratagies.main_event_loop import run_loop

STRATEGY_SELECTION = ('Select 1 to make a contract or '
                      '2 to make a project. To exit select 0')


class BaseAbstractStrategy:

    def __init__(self, name):
        self.name = name
        self.object = None

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class ContractStrategy(BaseAbstractStrategy):


    def create(self):
        self.object = Contract(name=self.name)

    def delete(self):
        del self.object


class ProjectStrategy(BaseAbstractStrategy):

    def create(self):
        self.object = Project(name=self.name)

    def delete(self):
        del self.object


class StrategyManager:

    def __init__(self, choice: int):
        self.choice = choice
        self.contract_strategy = ContractStrategy
        self.project_strategy = ProjectStrategy

    def get_strategy(self):
        if self.choice == 1:
            return self.contract_strategy
        return self.project_strategy

    def get_echo(self):
        strategy_name = 'Contract' if self.choice == 1 else 'Project'
        return f'You choose {strategy_name}'


@click.command()
@click.option(
    '--choice',
    prompt=STRATEGY_SELECTION,
    default=1
)
def choose_strategy(choice):
    chosen_strategy = None
    while chosen_strategy is None:
        if choice == 0:
            break
        elif choice == 1 or choice == 2:
            manager = StrategyManager(choice=choice)
            chosen_strategy = manager.get_strategy()
            click.echo(manager.get_echo())
        else:
            click.echo('Insert a correct answer')
            continue
    return chosen_strategy


if __name__ == '__main__':
    # run_loop()
    print('Hello from console program!')
    strategy = choose_strategy(standalone_mode=False)
    print(type(strategy))
