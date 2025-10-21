from textual.events import Key
from textual.screen import Screen
from textual.widgets import Button, Header
from textual.containers import Container, VerticalScroll

class FriendsScreen(Screen):
    TITLE="Friends"
    CSS_PATH = "css/friends.tcss"  

    requests_arrow = "^"
    friends_arrow = "^"

    requests = ["user 1", "user 2", "user 3", "user 4"]
    friends = ["user 1", "user 2", "user 3", "user 4"]

    def compose(self):
        yield Header()
        yield Container(
            Button(f"Requests          {self.requests_arrow}", id="requests-button"),
            Button(f"Friends          {self.friends_arrow}", id="friends-button"),
            id="friends-button-container"
        )


    async def on_button_pressed(self, event: Button.Pressed) -> None:

        def toggle_arrow(arrow):
            if(arrow == "⌄"):
                arrow = "^"
            else:
                arrow = "⌄"

            return arrow

        async def mount_scroll_widget(type):
            
            if(type == "requests"):
                list = self.requests
                id = "requests-list"
            else:
                list = self.friends
                id = "friends-list"

            v_scroll = VerticalScroll(id=id)
            container = self.query_one("#friends-button-container", Container)
            button = self.query_one(f"#{type}-button", Button)
            await container.mount(v_scroll, after=button)
            container.refresh()

            for i in list:
                v_scroll.mount(Button((f"{i}")))
            
            v_scroll.refresh()

        match event.button.id:

            case "requests-button": 
                self.requests_arrow = toggle_arrow(self.requests_arrow)
                requests_button = self.query_one("#requests-button", Button)
                requests_button.label = f"Requests          {self.requests_arrow}"
                requests_button.refresh()
                await mount_scroll_widget("requests")


            case "friends-button": 
                self.friends_arrow = toggle_arrow(self.friends_arrow)
                friends_button = self.query_one("#friends-button", Button)
                friends_button.label = f"Friends          {self.friends_arrow}"
                friends_button.refresh()      
                await mount_scroll_widget("friends")


class AddFriends(Screen):
    pass