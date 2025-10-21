from textual.events import Key
from textual.screen import Screen
from textual.widgets import Button, Header
from textual.containers import Container, VerticalScroll

class FriendsScreen(Screen):
    TITLE="Friends"
    CSS_PATH = "css/friends.tcss"  

    # used in buttons to represent toggling
    requests_arrow = "^"
    friends_arrow = "^"

    # flags for vertical scrolling containers 
    # once hidden flag turns false and widget is destroyed
    requests_vcontainer_flag = False
    friends_vcontainer_flag = False

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
                self.requests_vcontainer_flag = True
            else:
                list = self.friends
                id = "friends-list"
                self.friends_vcontainer_flag = True

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

                # updating toggle arrow
                self.requests_arrow = toggle_arrow(self.requests_arrow)
                requests_button = self.query_one("#requests-button", Button)
                requests_button.label = f"Requests          {self.requests_arrow}"
                requests_button.refresh()

                # handling container showing list of requests 
                if(self.requests_vcontainer_flag):
                    container = self.query_one("#requests-list")
                    await container.remove()
                    self.requests_vcontainer_flag = False
                else:
                    await mount_scroll_widget("requests")


            case "friends-button": 

                # updates the toggle arrow
                self.friends_arrow = toggle_arrow(self.friends_arrow)
                friends_button = self.query_one("#friends-button", Button)
                friends_button.label = f"Friends          {self.friends_arrow}"
                friends_button.refresh()      
                
                # handling container showing list of friends 
                if(self.friends_vcontainer_flag):
                    container = self.query_one("#friends-list")
                    await container.remove()
                    self.friends_vcontainer_flag = False
                else:
                    await mount_scroll_widget("friends")


class AddFriends(Screen):
    pass