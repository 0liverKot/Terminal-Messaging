from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Button, Header
from textual.containers import Container, Vertical

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
        
        match event.key:
            
            case "up": self.action_focus_previous()
            
            case "down": self.action_focus_next()

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