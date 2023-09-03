# import click
#
#
# @click.command()
# @click.option(
#     '--choice',
#     prompt=STRATEGY_SELECTION,
#     default=1
# )
# def choose_strategy(choice):
#     chosen_strategy = None
#     while chosen_strategy is None:
#         if choice == 0:
#             break
#         elif choice == 1 or choice == 2:
#             manager = StrategyManager(choice=choice)
#             chosen_strategy = manager.get_strategy()
#             click.echo(manager.get_echo())
#         else:
#             click.echo('Insert a correct answer')
#             continue
#     return chosen_strategy
#
#
# if __name__ == '__main__':
#     # run_loop()
#     print('Hello from console program!')
#     strategy = choose_strategy(standalone_mode=False)
#     print(type(strategy))
