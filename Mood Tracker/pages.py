from nicegui import ui
from config import MOOD_CONFIG

class MoodPageFactory:
    def __init__(self, entry_manager):
        self.entry_manager = entry_manager

    def create_page(self, mood_type):
        @ui.page(f'/{mood_type}_log')
        def mood_page():
            with ui.column().classes('w-full p-8 gap-8 mt-16'):
                ui.label(f'{mood_type.capitalize()} Daily Log')\
                    .classes('text-6xl font-bold text-center')
                
                with ui.grid(columns=2).classes('gap-8'):
                    self._create_input_section(mood_type)
                    self._create_history_section(mood_type)

    def _create_input_section(self, mood_type):
        with ui.card().classes('p-4'):
            ui.textarea('How are you feeling?').classes('w-full')
            ui.slider(min=1, max=10, value=5).classes('w-full')

    def _create_history_section(self, mood_type):
        with ui.card().classes('p-4'):
            ui.label('Previous Entries').classes('text-xl font-bold') 