from textual import events, on
from textual.app import ComposeResult
from textual.events import Key
from textual.screen import Screen
from textual.widgets import Button, Header, Input
from textual.reactive import var
from textual.containers import Container, VerticalScroll, Horizontal
from server.db.database import ROOT_URL
import requests
from common.account import Account
from client.chatroom import ChatroomScreen

class FriendsScreen(Screen):
    TITLE="Friends"
    CSS_PATH = "css/friends.tcss"  

    account: Account

    def __init__(self, account):
        super().__init__()
        self.account: Account = account

    
    # used in buttons to represent toggling
    requests_arrow = "^"
    friends_arrow = "^"

    # flags for vertical scrolling containers 
    # once hidden flag turns false and widget is destroyed
    requests_vcontainer_flag = False
    friends_vcontainer_flag = False
    
    friend_requests = None
    friends = None
    
    def get_friend_requests(self):
        result = requests.get(f"{ROOT_URL}requests/get_by_user/{self.account.get_username()}").json()
        return result


    def get_friends(self):
        result = requests.get(f"{ROOT_URL}friends/get_by_user/{self.account.get_username()}").json()
        return result


    def _on_mount(self) -> None:
        self.app.install_screen(AddFriends(self.account), "add friends")


    def compose(self) -> ComposeResult:
        
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

        if event.button.id == None:
            return

        def toggle_arrow(arrow):
            if(arrow == "⌄"):
                arrow = "^"
            else:
                arrow = "⌄"

            return arrow


        async def mount_scroll_widget(type, id, list):

            v_scroll = VerticalScroll(id=id)
            container = self.query_one("#friends-button-container", Container)

            if type == "friends":
                button = self.query_one(f"#add-friend-button", Button)
            else:
                button = self.query_one("#requests-button", Button)

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
                    button = Button(f"{i}", id=f"friend-{i}", classes="friends-scroll-button")
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
                    try:
                        container = self.query_one("#requests-list")
                        await container.remove()
                    except:
                        pass # if no requests then the container hadn't been made and cannot be found
                    
                    self.requests_vcontainer_flag = False
                else:
                    self.requests_vcontainer_flag = True
                    
                    # if no requests nothing is shown
                    list = self.get_friend_requests()
                    if(len(list) == 0):
                        return

                    await mount_scroll_widget("requests", "requests-list", list)


            case "friends-button": 

                # updates the toggle arrow
                self.friends_arrow = toggle_arrow(self.friends_arrow)
                friends_button = self.query_one("#friends-button", Button)
                friends_button.label = f"Friends          {self.friends_arrow}"
                friends_button.refresh()      
                
                # handling container showing list of friends
                if(self.friends_vcontainer_flag):
                    button = self.query_one("#add-friend-button")
                    await button.remove()
                    
                    try:
                        
                        container = self.query_one("#friends-list")
                        await container.remove()
                    except:
                        pass # if no friends then the container hasn't been made and count be found
                    self.friends_vcontainer_flag = False
                else:
                    
                    container = self.query_one("#friends-button-container", Container)
                    add_friends_button = Button("Add Friend", id="add-friend-button") 
                    await container.mount(add_friends_button)

                    self.friends_vcontainer_flag = True
                    
                    # if no friends nothing is shown
                    list = self.get_friends()
                    if(len(list) == 0):
                        return

                    await mount_scroll_widget("friends", "friends-list", list)

            case "add-friend-button":
                self.app.push_screen("add friends")


        if event.button.id.split("-")[0] == "friend":

            friend_name = event.button.id.split("-")[1]

            self.app.install_screen(ChatroomScreen(self.account, friend_name), "chatroom")
            self.app.push_screen("chatroom")

        try:
            if event.button.id is None:
                return 

            type = event.button.id.split("-")[0]
            if type not in ["accept", "decline", "request"]:
                return

            id = event.button.id.split("-")[1]
            match type:

            # pressing a request then replaces it with accept or decline buttons
                case "request":
                    container_id = f"container-{id}"           
                    container = self.query_one(f"#{container_id}", Horizontal)
                    event.button.remove()

                    container.mount(Button("✓", id=f"accept-{id}", classes="accept"))
                    container.mount(Button("x", id=f"decline-{id}", classes="decline"))

                    container.refresh()
                
                # accepting a friend request
                case "accept":
                    # delete the buttons 
                    button_container = self.query_one(f"#container-{id}", Horizontal)
                    button_container.remove()
                    
                    # add a new friend and delete the request
                    sender_name = id
                    recipient_name = self.account.get_username()
                    requests.post(f"{ROOT_URL}friends/create/{sender_name}/{recipient_name}")
                    requests.delete(f"{ROOT_URL}requests/delete/{sender_name}/{recipient_name}")
                
                # declining a friend request
                case "decline":
                    # delete the buttons 
                    button_container = self.query_one(f"#container-{id}", Horizontal)
                    button_container.remove()

                    sender_name = id
                    recipient_name = self.account.get_username()
                    requests.delete(f"{ROOT_URL}requests/delete/{sender_name}/{recipient_name}")
        except:
            pass


class AddFriends(Screen):
    
    TITLE="Add Friend"

    # users holds all the users in the app
    # once the user starts typing, users are filterd and added to display array

    users: list
    account: Account

    def __init__(self, account: Account):
        super().__init__()
        self.account: Account = account


    def on_mount(self) -> None:
        
        users = requests.get(f"{ROOT_URL}users/get").json()
        requests_recieved = requests.get(f"{ROOT_URL}requests/get_by_user/{self.account.username}").json()
        requests_sent = requests.get(f"{ROOT_URL}requests/get_sent/{self.account.username}").json()
        friends = requests.get(f"{ROOT_URL}friends/get_by_user/{self.account.username}").json()

        users.remove(self.account.username)


        for friend in friends:
            users.remove(friend)

        for request_recieved in requests_recieved : 
            users.remove(request_recieved)

        for request_sent in requests_sent: 
            users.remove(request_sent)

        self.users = users


    def compose(self) -> ComposeResult:

        yield Header()
        yield Container(
            Input(
                placeholder="Enter username... "
            ),
            VerticalScroll(
                id="users-vertical-scroll"
            ),
            id="new-friends-container"
        )

    # filter through list of users, mimicking a search
    @on(Input.Changed)
    async def filter_names(self, event: Input.Changed) -> None:
        
        value = event.value

        if(value == ""):
            display_names = []
        else: 
            # at most show ten users
            display_names = [x for x in self.users if x.startswith(value)]
            display_names = display_names[:10] 

        v_scroll_users = self.query_one("#users-vertical-scroll", VerticalScroll)

        for button in v_scroll_users.children:
            
            # button already exists so so remove from display names
            if (button.label in display_names): # type: ignore
                display_names.remove(button.label)    # type: ignore
            # button no longer in display names so remove 
            else:
                button.remove()

        for name in display_names:
            button = Button(f"{name}", id=f"addfriend-{name}")
            v_scroll_users.mount(button)

        v_scroll_users.refresh()

    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        
        if event.button.id == None:
            return

        try: 
            button_type = event.button.id.split("-")[0] 
        except:
            pass # incase some mysterious button is pressed to make sure program doesnt crash 


        if button_type == "addfriend":
            sender_name = self.account.username
            recipient_name = event.button.id.split("-")[1]

            # send request 
            requests.post(f"{ROOT_URL}requests/create/{sender_name}/{recipient_name}")

            event.button.remove()

            v_scroll_users = self.query_one("#users-vertical-scroll", VerticalScroll)
            v_scroll_users.refresh()