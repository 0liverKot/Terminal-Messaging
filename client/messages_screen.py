from textual.screen import Screen
from textual.app import ComposeResult
from common.account import Account
from textual.widgets import Header, Button
from textual.containers import VerticalScroll
from server.db.database import ROOT_URL

class MessagesScreen(Screen):
    TITLE="Messages"
    CSS_PATH="css/messages.tcss"
    

    account: Account

    def __init__(self, account):
        super().__init__()
        self.account = account

    def compose(self) -> ComposeResult:

        yield Header()

        previous_messages = 