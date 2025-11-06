from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Button, Header
from textual.containers import Container, Vertical
from client.friends_screen import FriendsScreen
from client.messages_screen import MessagesScreen
from common.account import Account
from typing import ClassVar
import sys

class MyApp(App[str]):
    TITLE = "Terminal Messaging"
    CSS_PATH="css/app.tcss"

    def __init__(self):
        
        # no specified account to use, hence use default 
        if len(sys.argv) == 1:
            self.account = Account("userdetails.json")
        else:
            self.account = Account(sys.argv[1])

        
        self.typing = False
        super().__init__()

    def compose(self) -> ComposeResult:

        yield Header()
        yield Container(
            Vertical(
                Button("Messages", id="message-button"),
                Button("Friends", id="friends-button"),
                Button("Exit", id="exit-button")
            ),
            id="button-container"
        )

    def on_mount(self) -> None:

        self.install_screen(FriendsScreen(self.account), name="friends")
        self.install_screen(MessagesScreen(self.account), name="messages")

    def on_key(self, event: events.Key) -> None:
        
        match event.key:
            
            case "up": self.action_focus_previous()
            
            case "down": self.action_focus_next()

            case "q": 
                if (not self.typing):
                    self.pop_screen()

        return 


    def on_button_pressed(self, event: Button.Pressed) -> None:

        match event.button.id:
            
            case "message-button": (
                self.push_screen("messages")
            )

            case "friends-button": (
                self.push_screen("friends")
            )

            case "exit-button": (
                self.exit()
            )


if __name__ == "__main__":
    app = MyApp()
    message = app.run()
    print(message)