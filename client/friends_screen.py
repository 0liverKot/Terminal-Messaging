from textual import events
from textual.events import Key
from textual.screen import Screen
from textual.widgets import Button, Header
from textual.containers import Container, VerticalScroll, Horizontal

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

    requests = ["oli", "dario", "remi", "trev"]
    friends = ["oli", "dario", "remi", "trev"]

    def compose(self):
        yield Header()
        yield Container(
            Button(f"Requests          {self.requests_arrow}", id="requests-button"),
            Button(f"Friends          {self.friends_arrow}", id="friends-button"),
            id="friends-button-container"
        )

    async def _on_key(self, event: Key) -> None:
        
        match event.key:

            case "escape":

                try:
                    if not (self.focused.classes.__contains__("accept") or self.focused.classes.__contains__("decline")): # type: ignore
                        return 
                except:    
                    return 
                
                # currently focused on an accept or decline button, replace it with the original request
                id = self.focused.id.split("-")[1] # type: ignore
                container = self.query_one(f"#container-{id}")

                # remove accept and decline buttons 
                await self.query_one(f"#accept-{id}", Button).remove()
                await self.query_one(f"#decline-{id}", Button).remove()

                await container.mount(Button(f"{id}", id=f"request-{id}", classes="request-scroll-button"))
                container.refresh()


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
            
                # container used for requests to replace the button with
                # accept or decline after pressing 
                if(type == "requests"):
                    button = Button(f"{i}", id=f"request-{i}", classes="requests-scroll-button")
                    request_container = Horizontal(id=f"container-{i}")
                    v_scroll.mount(request_container)
                    request_container.mount(button)

                else:
                    button = Button(f"{i}", classes="friends-scroll-button")
                    v_scroll.mount(button)
                
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

        try:
            # pressing a request then replaces it with accept or decline buttons
            if(event.button.id.split("-")[0] == "request"): # type: ignore

                id = event.button.id.split("-")[1] # type: ignore
                container_id = f"container-{id}"           
                container = self.query_one(f"#{container_id}", Horizontal)
                event.button.remove()

                container.mount(Button("✓", id=f"accept-{id}", classes="accept"))
                container.mount(Button("x", id=f"decline-{id}", classes="decline"))

                container.refresh()
        except:
            pass        

class AddFriends(Screen):
    pass