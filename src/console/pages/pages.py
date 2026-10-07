import os
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Center, Middle, Horizontal
from textual.widgets import Input, Label, Button, RichLog


class StartScreen(Screen):
    def compose(self) -> ComposeResult:
        ruta_actual = os.getcwd()
        
        with Middle():
            with Center():
                yield Label("LocalAI", id="titulo_inicio")
                yield Input(placeholder = "Escribir tu mensaje para empezar...", id = "input_inicio")
                yield Label(f"Ruta: {ruta_actual}", id="label_ruta")
                yield Button("Converacion", id="btn_conversacion", variant ="primary")
    
    def on_buttom_pressed(self, event: Button.Pressed) -> None:
        if event.buttom.id == "btn_conversacion":
            self.app.push_screen(ChatScreen())
            
class ChatScreen(Screen):
    def __init__(self, mensaje_inicial: str = ""):
        super().__init__()
        self.mensaje_inicial = mensaje_inicial

    def compose(self) -> ComposeResult:
        yield RichLog(id="historial_chat", wrap=True, highlight=True)
        
        with Horizontal(id="area_input"):
            yield Input(placeholder="Escribe tu mensaje aquí...", id="input_chat")
            yield Button("Enviar", id="btn_enviar", variant="success")

    def on_mount(self) -> None:
        log = self.query_one(RichLog)
        log.write("[bold green]=== Sesión LocalAI Iniciada ===[/bold green]")
        
        if self.mensaje_inicial:
            self.enviar_mensaje(self.mensaje_inicial)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.enviar_mensaje(event.value)
        event.input.value = ""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_enviar":
            caja_texto = self.query_one("#input_chat", Input)
            self.enviar_mensaje(caja_texto.value)
            caja_texto.value = ""

    def enviar_mensaje(self, texto: str) -> None:
        if not texto.strip():
            return
            
        log = self.query_one(RichLog)
        log.write(f"\n[bold cyan]Tú:[/bold cyan] {texto}")
        
        # TODO: Aquí es donde usaremos @work de Textual para llamar a src/services/
        # sin que se congele la interfaz gráfica.
        log.write("[bold magenta]IA:[/bold magenta] (Generando respuesta...)")    
        
