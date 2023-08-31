from datetime import datetime


class Order:
    def __init__(self, name):
        self.name: str = name
        self.status = 'draft'
        self.sign_at = None

    def approve(self):
        self.status = 'active'
        self.created_at = datetime.now()

    def finish(self):
        self.status = 'finished'

    def set_sign_at(self) -> None:
        self.sign_at = datetime.now()

    def set_created_at(self) -> None:
        self.created_at = datetime.now()


class Project:
    order_links: list
