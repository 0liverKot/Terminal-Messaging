import json
from textual import on, work
from textual.app import ComposeResult
from textual.events import Compose, Key
from textual.screen import Screen
from textual.widgets import Header, Input, Label
from textual.containers import VerticalScroll, Container
from server.db.database import ROOT_URL
import requests
import threading
import websockets
import asyncio
from common.account import Account

class ChatroomScreen(Screen):
    TITLE: str
    CSS_PATH = "css/chatroom.tcss"

    account: Account

    username: str
    friend_name: str

    websocket: websockets.ClientConnection
    messages: list[dict[str, str]]
    conversation_id: int

    def __init__(self, account: Account, friend_name: str):
        super().__init__()
        self.account: Account = account

        self.title = f"Chat With {friend_name.capitalize()}"

        if account.username is None:
            raise Exception("username not defined")
        
        self.username = account.username
        self.friend_name = friend_name

    # using this ensures self.username has already been set
    # needed for use in on_mount incase it runs before __init__
    def get_username(self):
        while True:
            if self.username is None:
                pass
            else: 
                return self.username

    def compose(self) -> ComposeResult:
        yield Header()


    async def _on_mount(self) -> None:

        # socket running in background
        self.run_worker(self.listen_socket(self.username, self.friend_name), thread=True)

        response = requests.get(
            f"{ROOT_URL}friends/get_friendship/{self.friend_name}/{self.username}"
            )
        friendship_json = response.json()
        
        response = requests.get(
            f"{ROOT_URL}conversations/get/{friendship_json["conversation_id"]}", json=friendship_json)
        conversation_json = response.json()
        self.messages = conversation_json["messages"]
        self.conversation_id = conversation_json["id"]

        messages_container = VerticalScroll(id="messages-container")
        message_input = Input(id="message-input", valid_empty=False)
        await self.mount(messages_container)
        
        await self.mount(message_input)
        await self.fill_messages_container()


    async def fill_messages_container(self):         

        for message in self.messages:
            if message == {}:
                continue

            await self.add_message(message)


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


    async def add_message(self, message: dict[str, str]):
        sender = message["sender"]
        text = message["text"]

        if sender == self.username:
            message_class = "user"
        else:
            message_class = "friend"

        messages_container = self.query_one("#messages-container", VerticalScroll)

        message_container = Container(classes=f"{message_class}")
        await messages_container.mount(message_container)
        await message_container.mount(Label(content=f"{sender}"))
        await message_container.mount(Label(content=f"{text}"))


    async def listen_socket(self, user: str, friend: str):
        
        # chat_room is sorted identically to maintain consistency
        users = sorted([user, friend])
        chat_room = f"{users[0]}-{users[1]}"
        username = self.get_username()
        async with websockets.connect(f"ws://localhost:8000/ws/{username}") as ws:
            await ws.send(chat_room)
            self.websocket = ws

            async def receive_mesages():
                while True:
                    message = await ws.recv()
                    message_json = json.loads(message)
                    dict = {"sender": friend, "text": list(message_json.values())[1]}
                    await self.add_message(dict)


            await asyncio.gather(receive_mesages())


    @on(Input.Submitted)
    async def input_submit(self) -> None:
        
        input = self.query_one(Input)
        message_dict = {"sender": self.username, "text": input.value}  
        input.clear()

        await self.add_message(message_dict)
        await self.websocket.send(json.dumps(message_dict))

        requests.put(f"{ROOT_URL}conversations/add_message/{self.conversation_id}", json=message_dict)

