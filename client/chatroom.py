from textual.app import ComposeResult
from textual.events import Compose, Key
from textual.screen import Screen
from textual.widgets import Button, Header, Input, Label
from textual.containers import Vertical
from server.db.database import ROOT_URL
import requests
import threading
import websockets
import asyncio
from common.account import Account

class ChatroomScreen(Screen):
    TITLE: str
    CCS_PATH = "css/chatroom.tcss"

    account: Account

    username: str
    friend_name: str

    messages: list[dict[str, str]]

    def __init__(self, account: Account, friend_name: str):
        super().__init__()
        self.account: Account = account

        self.title = f"Chat With {friend_name.capitalize()}"

        if account.username is None:
            raise Exception("username not defined")
        
        self.username = account.username
        self.friend_name = friend_name


    def compose(self) -> ComposeResult:
        yield Header()


    async def _on_mount(self) -> None:

        # socket runnint in background
        threading.Thread(target=self.listen_socket, daemon=True, args=(self.username, self.friend_name)).start()

        response = requests.get(
            f"{ROOT_URL}friends/get_friendship/{self.friend_name}/{self.username}"
            )
        friendship_json = response.json()
        
        response = requests.get(
            f"{ROOT_URL}conversations/get/conversation_with", json=friendship_json)
        conversation_json = response.json()
        self.messages = conversation_json["messages"]

        messages_container = Vertical(id="messages-container")
        message_input = Input(id="message-input")
        await self.mount(messages_container)
        await self.mount(message_input)
        await self.fill_messages_container()


    async def fill_messages_container(self):         

        messages_container = self.query_one("#messages-container")
        
        for message in self.messages:
            await messages_container.mount(Label(content=f"{message.values}"))


    def _on_key(self, event: Key) -> None:
        if event.key == None:
            return 
        
        match event.key:
            case "escape":

                if self.focused == None:
                    return

                if not (self.focused.id == "message-input"):
                    return
                
                self.set_focus(None)


    async def listen_socket(self, user: str, friend: str):
        
        # chat_room is sorted identically to maintain consistency
        users = sorted([user, friend])
        chat_room = f"{users[0]}-{users[1]}"
        async with websockets.connect("ws://localhost:8000/ws") as ws:
            await ws.send(chat_room)

            async def send_messages():
                pass

            async def receive_mesages():
                pass

            await asyncio.gather(send_messages(), receive_mesages())

