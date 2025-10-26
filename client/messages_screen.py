from textual.screen import Screen
from common.account import Account

class MessagesScreen(Screen):
    
    account: Account

    def __init__(self, account):
        super().__init__()
        self.account = account