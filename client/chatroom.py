from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Input
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

    def __init__(self, account: Account, friend_name: str):
        super().__init__()
        self.account: Account = account

        if account.username is None:
            raise Exception("username not defined")
        
        self.username = account.username
        self.friend_name = friend_name


    def _on_mount(self) -> None:

        # socket runnint in background
        threading.Thread(target=self.listen_socket, daemon=True, args=(self.username, self.friend_name)).start()

        response = requests.get(
            f"{ROOT_URL}friends/get_friendship/{self.friend_name}/{self.username}"
            )
        friendship_json = response.json()
        
        response = requests.get(
            f"{ROOT_URL}conversations/get/conversation_with", json=friendship_json)
        conversation_json = response.json()
        messages = conversation_json["messages"]


    async def listen_socket(self, user: str, friend: str):
        
        # chat_room is sorted identically to maintain consistency
        chat_room = sorted([user, friend]) 
        async with websockets.connect("ws://localhost:6767") as ws:
            await ws.send(chat_room)

            async def send_messages():
                pass

            async def receive_mesages():
                pass

            await asyncio.gather(send_messages(), receive_mesages())

