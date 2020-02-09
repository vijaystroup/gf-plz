from time import sleep
from controller import Controller


if __name__ == '__main__':
    controller = Controller()
    controller.login()
    sleep(5)
    # controller.auto_swipe()
