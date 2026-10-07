from textual.app import App
from src.console.pages.pages import StartScreen

class LocalAIApp(App):
    CSS = """
    StartScreen {
        align: center middle;
    }
    #titulo_inicio {
        text-align: center;
        text-style: bold;
        padding-bottom: 1;
    }
    #input_inicio {
        width: 60;
        margin_bottom: 1;
    }
    #label_ruta {
        text-align: center;
        padding-bottom: 1;
        color: $text-muted;
    }
    #historial_chat {
        height: 1fr;
        border: round $primary;
        margin: 1;
    }
    #area_input {
        height: 3;
        dock: bottom;
        margin: 0 1 1 1;
    }
    #input_chat {
        width: 1fr;
    }    
    """
    
    def on_mount(self) -> None:
        self.push_screen(StartScreen())
    