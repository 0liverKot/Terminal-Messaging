from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Button, Header
from textual.containers import Container, Vertical
from enum import Enum 

class MyApp(App[str]):
    TITLE = "Terminal Messaging"
    CSS_PATH="css/app.tcss"

    focus_intialised = False

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

    def on_key(self, event: events.Key) -> None:

        # on the first press of either up or down arrow message is focused
        # user can then use arrows to select other options
        if(not self.focus_intialised and (event.key == "up" or event.key == "down")):
            self.focus_intialised = True
            message_button = self.query_one("#message-button")
            message_button = message_button.focus
            return
        
        # changing focus to different buttons with arrows
        if(event.key == "up" or event.key == "down"):

            buttons = {
                1: self.query_one("#message-button"),
                2: self.query_one("#friends-button"),
                3: self.query_one("#exit-button")
            }
            

            focused = self.focused;
            current_index = [key for key, value in buttons.items() if value == focused][0]

            match event.key:
                case "up": current_index -= 1
                case "dowen": current_index += 1

            # check if current index is valid 
            if(current_index < 1 or current_index > 3):
                return;

            buttons[current_index] = buttons[current_index].focus
            return


    def on_button_pressed(self, event: Button.Pressed) -> None:

        match event.button.id:
            
            case "message-button": (

            )

            case "friends-button": (
            
            )

            case "exit-button": (
                self.exit()
            )
                
if __name__ == "__main__":
    app = MyApp()
    message = app.run()
    print(message)