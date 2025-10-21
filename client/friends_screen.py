from textual.events import Key
from textual.screen import Screen
from textual.widgets import Button, Header
from textual.containers import Container, Horizontal

class FriendsScreen(Screen):
    TITLE="Friends"
    CSS_PATH = "css/friends.tcss"  

    requests_arrow = "⌄"
    friends_arrow = "⌄"


    def compose(self):
        yield Header()
        yield Container(
            Button(f"Requests          {self.requests_arrow}", id="requests-button"),
            Button(f"Friends          {self.friends_arrow}", id="friends-button"),
            id="friends-button-container"
        )


    def on_button_pressed(self, event: Button.Pressed) -> None:

        def toggle_arrow(arrow):
            if(arrow == "⌄"):
                arrow = "^"
            else:
                arrow = "⌄"

            return arrow

        match event.button.id:

            case "requests-button": 
                self.requests_arrow = toggle_arrow(self.requests_arrow)
                requests_button = self.query_one("#requests-button", Button)
                requests_button.label = f"Requests          {self.requests_arrow}"
                requests_button.refresh()

            case "friends-button": 
                self.friends_arrow = toggle_arrow(self.friends_arrow)
                friends_button = self.query_one("#friends-button", Button)
                friends_button.label = f"Friends          {self.friends_arrow}"
                friends_button.refresh()      



class AddFriends(Screen):
    pass