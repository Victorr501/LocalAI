from src.console.pages.local_ai_app_css import LocalAIApp

def iniciar_terminal(ai_engine, db):
    app = LocalAIApp()
    app.run()