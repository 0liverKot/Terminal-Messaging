import requests
from textual.events import Event
from textual.screen import Screen
from textual.app import ComposeResult
from common.account import Account
from textual.widgets import Header, Button
from textual.containers import VerticalScroll
from server.db.database import ROOT_URL
from client.chatroom import ChatroomScreen

class MessagesScreen(Screen):
    TITLE="Messages"
    CSS_PATH="css/messages.tcss"
    

    account: Account

    def __init__(self, account):
        super().__init__()
        self.account = account

    def on_mount(self) -> None:

        self.mount(Header())
        previous_conversations = requests.get(f"{ROOT_URL}conversations/get/non_empty_conversations/{self.account.username}").json()

        self.mount(VerticalScroll(id="v-scroll-messages"))
        v_scroll = self.query_one("#v-scroll-messages")

        for conversation in previous_conversations:
            button = Button(f"{conversation["friend"]}", id=f"{conversation["friend"]}")
            v_scroll.mount(button)


    def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button.id == None:
            return
        
        friend_name = event.button.id
        self.app.install_screen(ChatroomScreen(self.account, friend_name), "chatroom") 
        self.app.push_screen("chatroom")


        
