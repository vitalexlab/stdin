from src.event_loop.main_loop import MainLoop

if __name__ == '__main__':
    loop = MainLoop()
    try:
        while True:
            loop.run()
            new_session = input(
                'Start a new one? (Choose 1 to start and 0 to exit): '
            )
            if not bool(new_session) or new_session == '0':
                print('See you!')
                break
            continue
    except KeyboardInterrupt:
        print('')
        print('See you!')
