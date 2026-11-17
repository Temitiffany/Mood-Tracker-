from nicegui import ui

class MoodUI:
    @staticmethod
    def create_card(content, style_config):
        return ui.card().classes('p-4')
    
    @staticmethod
    def create_mood_slider(on_change, config):
        return ui.slider(min=1, max=10, value=5, on_change=on_change) 