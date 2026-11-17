from nicegui import ui
from datetime import datetime
import json
import os
import random
import time
from typing import List

# Emoji constants
EMOJI = {
    'task': '📝', 'time': '⏰', 'delete': '❌', 'add': '➕',
    'clear': '🧹', 'new_day': '🌅', 'completed': '✅',
    'incomplete': '⭕️', 'success': '✨', 'earth': '🌍', 'save': '💝'
}

# Represents a single task
class TaskItem:
    def __init__(self, text: str = "", time: str = "", completed:str = "undone"):
        self.text = text
        self.time = time
        self.completed = completed
        self.card = None
        self.complete_button = None
        self.undo_button = None

# Main tracker class
class DailyMe:
    def __init__(self):
        self.tasks: List[TaskItem] = []
        self.data_file = 'daily_me_data.json'
        self.setup_background()
        self.setup_home_page()
        self.setup_ui()
        self.load_tasks()
        

    def setup_background(self):
        ui.add_head_html('''
            <style>
                body {
                    margin: 0;
                    overflow: auto;
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                }
                #particles-js {
                    position: unfixed;
                    width: 100%;
                    height: 100%;
                    z-index: -1;
                }
                .glass-card {
                    background: rgba(255, 255, 255, 0.15);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }
                .task-card {
                    transition: all 0.3s;
                }
                .task-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                }
                .completed-task {
                    opacity: 0.7;
                    text-decoration: line-through;
                    background: rgba(200, 255, 200, 0.2);
                }
                @keyframes shake {
                    0%, 100% { transform: translateX(0); }
                    20%, 60% { transform: translateX(-5px); }
                    40%, 80% { transform: translateX(5px); }
                }
                .shake { animation: shake 0.5s; }
                .home-background {
                    position: relative;
                    background-image: url('https://i.pinimg.com/736x/27/45/b6/2745b65de45f2cab4e6656e4cbef81e2.jpg');
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    min-height: 100vh;
                    width: 100vw;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                }
                .home-background::before {
                    content: '';
                    position: absolute;
                    top: 0; left: 0; right: 0; bottom: 0;
                    background: rgba(30, 30, 40, 0.45);
                    z-index: 0;
                }
                .home-container {
                    position: relative;
                    z-index: 1;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                    padding: 2rem 3rem;
                    background: rgba(255, 255, 255, 0.18);
                    border-radius: 28px;
                    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                    backdrop-filter: blur(16px);
                    border: 1.5px solid rgba(255,255,255,0.25);
                    animation: fadeIn 1.2s cubic-bezier(.39,.575,.56,1.000);
                }
                @keyframes fadeIn {
                    0% { opacity: 0; transform: translateY(40px) scale(0.98); }
                    100% { opacity: 1; transform: translateY(0) scale(1); }
                }
                .app-title {
                    font-size: 4rem;
                    font-weight: bold;
                    color: white;
                    text-shadow: 0 0 18px rgba(0, 0, 0, 0.7);
                    margin-bottom: 0.5rem;
                    letter-spacing: 2px;
                    animation: fadeIn 1.5s 0.2s backwards;
                }
                .app-subtitle {
                    font-size: 1.5rem;
                    color: #f3f3f3;
                    margin-bottom: 1.5rem;
                    text-shadow: 0 2px 8px rgba(0,0,0,0.25);
                    font-weight: 400;
                    animation: fadeIn 1.5s 0.4s backwards;
                }
                .start-button {
                    background: linear-gradient(90deg, #6dd5ed 0%, #2193b0 100%);
                    border: none;
                    color: white;
                    font-size: 1.5rem;
                    padding: 1rem 2.5rem;
                    border-radius: 50px;
                    transition: all 0.3s ease;
                    margin-top: 1.5rem;
                    font-weight: bold;
                    letter-spacing: 1px;
                    box-shadow: 0 4px 24px 0 rgba(33,147,176,0.25);
                    text-shadow: 0 2px 8px rgba(0,0,0,0.18);
                    animation: fadeIn 1.5s 0.6s backwards;
                }
                .start-button:hover {
                    background: linear-gradient(90deg, #2193b0 0%, #6dd5ed 100%);
                    transform: translateY(-5px) scale(1.07);
                    box-shadow: 0 10px 32px rgba(33,147,176,0.35);
                }
                @media (max-width: 600px) {
                    .app-title { font-size: 2.2rem; }
                    .app-subtitle { font-size: 1.1rem; }
                    .home-container { padding: 1.2rem 0.5rem; }
                    .start-button { font-size: 1.1rem; padding: 0.7rem 1.2rem; }
                }
            </style>
            <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    particlesJS('particles-js', {
                        particles: {
                            number: { value: 60, density: { enable: true, value_area: 800 } },
                            color: { value: "#ffffff" },
                            shape: { type: "circle" },
                            opacity: { value: 0.5, random: true },
                            size: { value: 3, random: true },
                            line_linked: { enable: true, distance: 150, color: "#ffffff", opacity: 0.4, width: 1 },
                            move: { enable: true, speed: 1, direction: "none", random: true }
                        },
                        interactivity: {
                            detect_on: "canvas",
                            events: {
                                onhover: { enable: true, mode: "grab" },
                                onclick: { enable: true, mode: "push" }
                            }
                        }
                    });
                });
            </script>
        ''')
        ui.html('<div id="particles-js"></div>').classes('fixed top-0 left-0 w-full h-full')

    def setup_home_page(self):
        @ui.page('/')
        def home():
            with ui.column().classes('home-background'):
                with ui.column().classes('home-container'):
                    ui.label('Daily Me').classes('app-title')
                    ui.label('Your personal journey, one day at a time.').classes('app-subtitle')
                    ui.button('Start', on_click=lambda: ui.open('/entries')) \
                        .classes('start-button')

    def setup_ui(self):
        ui.page_title("Daily Me")

        with ui.column().classes("w-full max-w-2xl mx-auto p-4 gap-4"):
            with ui.card().classes("glass-card w-full p-4"):
                ui.label(f"{EMOJI['earth']} Daily Me {EMOJI['earth']}") \
                    .classes("text-2xl font-bold text-center text-blue")

            with ui.card().classes("glass-card w-full p-4"):
                with ui.row().classes("w-full items-center gap-2"):
                    self.task_input = ui.input(f"{EMOJI['task']} Task").classes("flex-grow bg-blue/90")
                    self.time_input = ui.input(f"{EMOJI['time']} Time (e.g., 09:00)").classes("w-32 bg-blue/90")
                    ui.button(f"{EMOJI['add']} Add", on_click=self.add_task) \
                        .classes("bg-green-500 hover:bg-green-600 text-white")

            self.task_container = ui.column().classes("w-full gap-2")

            with ui.card().classes("glass-card w-full p-2"):
                with ui.row().classes("w-full justify-center gap-4"):
                    ui.button(f"{EMOJI['save']} Save Selected", on_click=self.save_all_tasks)\
                        .classes("bg-green-500 hover:bg-blue-600 text-white")
                    ui.button(f"{EMOJI['clear']} Clear All", on_click=self.clear_all_tasks) \
                        .classes("bg-red-500 hover:bg-red-600 text-white")
                    ui.button(f"{EMOJI['new_day']} New Day", on_click=self.clear_all_tasks) \
                        .classes("bg-blue-500 hover:bg-blue-600 text-white")

    def add_task(self):

        task_text = self.task_input.value.strip()
        time_text = self.time_input.value.strip()

        if not task_text:
            self.shake_input(self.task_input)
            return

        if time_text and not self.validate_time(time_text):
            self.shake_input(self.time_input)
            return

        # Clear inputs after task is successfully added
        self.task_input.value = ""
        self.time_input.value = ""

        self.celebrate_add()
                                                
        task = TaskItem(text=task_text, time=time_text, completed="undone")
        self.tasks.append(task)
        self.display_task(task)
        self.save_tasks()
        

   
    def display_task(self, task: TaskItem):
        with ui.card().classes("task-card w-full p-2 bg-blue/90") as card:
            task.card = card
            with ui.row().classes("w-full items-center justify-between gap-2"):
                status = ui.label().classes("text-xl")

                def update_status_display():
                    if task.completed == "done":
                        status.text = EMOJI["completed"]
                    else:
                        status.text = EMOJI["incomplete"]

                update_status_display()

                task_label = ui.label(f"{EMOJI['task']} {task.text}").classes("flex-grow")
                task_label.bind_class_from(task, "completed", lambda c: "completed-task" if task.completed == "done" else "")

                ui.label(f"{EMOJI['time']} {task.time}").classes("text-sm text-gray-600")

                # Complete and undo buttons
                task.complete_button = ui.button("✅", on_click=lambda: self.mark_done(task)).classes("text-green-600")
                task.undo_button = ui.button("❎", on_click=lambda: self.mark_undone(task)).classes("text-yellow-600")
                task.save_button = ui.button("❌", on_click=lambda: self.mark_undone(task)).classes("text-red-600")

                # Delete
                task.delete_button = ui.button(EMOJI["delete"], on_click=lambda: self.delete_task(task)).classes("text-red-500")

                update_status_display()

    
    def mark_done(self, task: TaskItem):
        task.completed = "done"
        self.save_tasks()
        self.celebrate_completion(task)
        task.card.clear()
        self.display_task(task)

    def mark_undone(self, task: TaskItem):
        task.completed = "undone"
        self.save_tasks()
        task.card.clear()
        self.display_task(task)

    def save_all_tasks(self):
        for task in self.task[:]:
            task.card.save()
        self.tasks.save()
        self.save_tasks()


    def delete_task(self, task: TaskItem):
        self.tasks.remove(task)
        task.card.delete()
        self.save_tasks()  # <-- Add here

                       
    def clear_all_tasks(self):
        for task in self.tasks[:]:
            task.card.delete()
        self.tasks.clear()
        self.save_tasks()

    def on_task_complete(self, task: TaskItem):
        self.save_tasks()
        if task.completed:
            self.celebrate_completion(task)

    def validate_time(self, time_str: str) -> bool:
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False

    def shake_input(self, element: ui.input):
        element.classes("shake")
        time.sleep(0.5)
        element.classes(remove="shake")

    def celebrate_add(self):
        ui.notify("Task added!", type="positive")
        ui.run_javascript('confetti({ particleCount: 100, spread: 70 });')

    def celebrate_completion(self, task: TaskItem):
        ui.notify("Task completed!", type="positive")
        ui.run_javascript(f'''
            const rect = document.getElementById("{task.card.id}").getBoundingClientRect();
            confetti({{
                particleCount: 30,
                spread: 40,
                origin: {{ 
                    x: (rect.left + rect.width/2) / window.innerWidth,
                    y: (rect.top + rect.height/2) / window.innerHeight
                }}
            }});
        ''')

    def load_tasks(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r") as f:
                    tasks = json.load(f)
                    for task_data in tasks:
                        task = TaskItem(
                            text=task_data["text"],
                            time=task_data["time"],
                            completed=task_data.get("completed", "undone"))
                        self.tasks.append(task)
                        self.display_task(task)
        except Exception as e:
            ui.notify(f"Error loading tasks: {e}", type="negative")


    def save_tasks(self):
        try:
            task_data = [{
                "text": task.text,
                "time": task.time,
                "completed": task.completed  # "done" or "undone"
            } for task in self.tasks]
            
            with open(self.data_file, "w") as f:
                json.dump(task_data, f, indent=4)
        except Exception as e:
            ui.notify(f"Error saving tasks: {e}", type="negative")


# Confetti script and run
ui.add_head_html('<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>')
DailyMe()
ui.run(title="Daily Me", favicon="📝", dark=True)


