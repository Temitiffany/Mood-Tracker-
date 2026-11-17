from nicegui import ui
from config import MOOD_CONFIG
from components import MoodUI
from managers import MoodEntryManager
from pages import MoodPageFactory
import json
import os

from datetime import datetime

# Create a navigation bar component
def create_nav_bar():
    with ui.row().classes('w-full justify-between items-center p-4 fixed top-0 left-0 z-50').style('backdrop-filter: blur(10px); background: rgba(0,0,0,0.3);'):
        # Left side - Logo/Home
        with ui.link(target='/').classes('flex items-center gap-2 text-white no-underline'):
            ui.icon('home').classes('text-2xl')
            ui.label('Mood Tracker').classes('text-xl font-bold')
        
        # Center - Main Navigation
        with ui.row().classes('gap-6'):
            ui.link('Mood Board', target='/mood_board').classes(
                'text-white/90 hover:text-white transition-colors px-4 py-2 rounded-full hover:bg-white/10'
            )
            ui.link('Summary', target='/mood_summary').classes(
                'text-white/90 hover:text-white transition-colors px-4 py-2 rounded-full hover:bg-white/10'
            )
        
        # Right side - Quick Actions
        with ui.row().classes('gap-4'):
            for mood in ['Joy', 'Sadness', 'Anger', 'Fear', 'Anxiety', 'Disgust']:
                with ui.link(target=f'/{mood.lower()}_log').classes('w-8 h-8 flex items-center justify-center rounded-full transition-transform hover:scale-110').style(f'background: {colors[mood.lower()]["primary"]}33;'):
                    ui.icon('edit').tooltip(f'Log {mood}').classes('text-white/90')

# Home Page
@ui.page('/')
def home():
    create_nav_bar()  # Add navigation bar
    with ui.column().classes('w-full min-h-screen items-center justify-center p-8 gap-8 mt-16'):
        # Main content card with glass effect
        with ui.card().classes('max-w-2xl w-full p-8').style('''
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 1rem;
        '''):
            # Animated welcome section
            with ui.column().classes('items-center gap-4 animate-fade-in'):
                ui.label('Welcome to').classes('text-2xl text-white/80')
                ui.label('Mood Tracker').classes('text-6xl font-bold text-white text-center')
                ui.label('Your emotional wellness companion').classes('text-xl text-white/80 mt-2')

            ui.separator().classes('my-8')

            # Quick actions
            with ui.grid(columns=2).classes('gap-4 w-full mt-4'):
                with ui.link(target='/mood_board'):
                    with ui.card().classes('p-6 hover:scale-105 transition-transform cursor-pointer bg-white/10'):
                        ui.label('Track Mood').classes('text-xl font-bold text-white')
                        ui.label('Record and monitor your emotions').classes('text-sm text-white/80')

                with ui.link(target='/mood_summary'):
                    with ui.card().classes('p-6 hover:scale-105 transition-transform cursor-pointer bg-white/10'):
                        ui.label('View Summary').classes('text-xl font-bold text-white')
                        ui.label('Analyze your emotional patterns').classes('text-sm text-white/80')

            # Resources section
            with ui.column().classes('w-full mt-8 gap-4'):
                ui.label('Helpful Resources').classes('text-2xl font-bold text-white text-center')
                
                with ui.grid(columns=2).classes('gap-4 mt-4'):
                    with ui.card().classes('p-4 bg-white/10'):
                        ui.link('Mental Health Tips', 'https://www.who.int/news-room/fact-sheets/detail/mental-health-strengthening-our-response')
                        ui.label('World Health Organization').classes('text-sm text-white/60')

                    with ui.card().classes('p-4 bg-white/10'):
                        ui.link('Meditation Guide', 'https://www.mindful.org/how-to-meditate/')
                        ui.label('Mindful.org').classes('text-sm text-white/60')

                    with ui.card().classes('p-4 bg-white/10'):
                        ui.link('Stress Management', 'https://www.helpguide.org/articles/stress/stress-management.htm')
                        ui.label('HelpGuide.org').classes('text-sm text-white/60')

                    with ui.card().classes('p-4 bg-white/10'):
                        ui.link('Emergency Help', 'https://www.betterhelp.com/gethelpnow/')
                        ui.label('Crisis Resources').classes('text-sm text-white/60')

    # Add animations and styling
    ui.add_head_html('''
        <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .animate-fade-in {
            animation: fadeIn 1s ease-out;
        }

        body {
            margin: 0;
            padding: 0;
            min-height: 100vh;
            background-image: url("https://www.ixpap.com/images/2024/06/Inside-Out-2-Wallpaper-7.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            font-family: 'Poppins', sans-serif;
        }

        /* Add hover effects */
        .card {
            transition: all 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        </style>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    ''')

# Mood Board Page
@ui.page('/mood_board')
def mood_board_page():
    create_nav_bar()  # Add navigation bar
    with ui.column().classes('w-full items-center justify-center py-12 mt-16'):
        # Title section with custom styling
        with ui.column().classes('w-full items-center justify-center py-12'):
            ui.label('How are we feeling today?').classes('text-6xl font-bold text-white text-center')\
                .style('text-shadow: 2px 2px 4px rgba(0,0,0,0.3); font-family: "Poppins", sans-serif;')
            ui.label('Choose your current emotion below').classes('text-2xl text-white/80 mt-4 text-center')\
                .style('text-shadow: 1px 1px 2px rgba(0,0,0,0.2);')

        moods = {
            "Joy": "https://i.pinimg.com/736x/d2/62/a4/d262a47edca42a16da6b63d6b80c51eb.jpg",
            "Sadness": "https://i.pinimg.com/736x/71/9f/d4/719fd454f8e0c3e25177e491bf6d6772.jpg",
            "Anger": "https://i.pinimg.com/736x/e5/d6/c7/e5d6c773dbac5526ae41f45200d95725.jpg",
            "Fear": "https://i.pinimg.com/736x/78/12/be/7812bef9ce2a238f1e6560a94a2f71a5.jpg",
            "Disgust": "https://i.pinimg.com/736x/98/07/9a/98079a1ace807a8b8c9caf8ae54f12e0.jpg",
            "Anxiety": "https://i.pinimg.com/736x/b4/6c/d1/b46cd1eb06e223db4e65b635c4b0191d.jpg",
        }

        # Add custom CSS for floating animation
        ui.add_head_html('''
            <style>
            .character-container {
                animation: float 3s ease-in-out infinite;
                transition: all 0.3s ease;
                display: flex;
                flex-direction: column;
                align-items: center;
                text-decoration: none;
            }
            
            @keyframes float {
                0% { transform: translateY(0px); }
                50% { transform: translateY(-10px); }
                100% { transform: translateY(0px); }
            }
            
            .character-container:hover {
                transform: scale(1.1);
                cursor: pointer;
            }
            
            .character-image {
                border-radius: 50%;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
                width: 12rem;
                height: 12rem;
                object-fit: cover;
            }
            
            .character-container:hover .character-image {
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
            }
            
            .character-label {
                margin-top: 1rem;
                color: white;
                font-size: 1.25rem;
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                opacity: 0;
                transform: translateY(10px);
                transition: all 0.3s ease;
            }
            
            .character-container:hover .character-label {
                opacity: 1;
                transform: translateY(0);
            }
            </style>
        ''')

        with ui.grid(columns=6).classes('gap-8 p-8'):
            for mood_name, img_path in moods.items():
                with ui.link(target=f'/{mood_name.lower()}_log').classes('character-container'):
                    ui.image(img_path).classes('character-image')
                    ui.label(mood_name).classes('character-label')

        # Page background
        ui.add_head_html('''
            <style>
            body {
                margin: 0;
                padding: 0;
                min-height: 100vh;
                width: 100%;
                background-image: url("https://i.pinimg.com/736x/c7/34/4a/c7344a52a43af7d51d94ffb5893f171c.jpg");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            </style>
        ''')

# Mood Summary Page
@ui.page('/mood_summary')
def mood_summary_page():
    create_nav_bar()  # Add navigation bar
    with ui.column().classes('w-full min-h-screen p-8 items-center gap-8 mt-16'):
        ui.label('Mood Summary & Analytics').classes('text-4xl font-bold text-white text-center p-8')

        def calculate_mood_stats():
            all_moods = []
            for mood_type, mood_entries in entries.items():
                for entry in mood_entries:
                    if isinstance(entry, dict) and 'timestamp' in entry:
                        entry_date = datetime.strptime(entry['timestamp'].split()[0], '%Y-%m-%d')
                        all_moods.append({
                            'type': mood_type,
                            'intensity': entry.get('intensity', 5),
                            'date': entry_date,
                            'text': entry.get('text', '')
                        })
            return sorted(all_moods, key=lambda x: x['date'], reverse=True)

        with ui.card().classes('w-full p-6 bg-white/90'):
            with ui.tabs().classes('w-full') as tabs:
                ui.tab('Weekly Overview')
                ui.tab('Mood Distribution')
                ui.tab('Tips & Recommendations')

            with ui.tab_panels(tabs, value='Weekly Overview').classes('w-full'):
                with ui.tab_panel('Weekly Overview'):
                    mood_stats = calculate_mood_stats()
                    if mood_stats:
                        with ui.column().classes('gap-4'):
                            for entry in mood_stats[:7]:  # Show last 7 entries
                                with ui.card().classes(f'p-4 border-l-4').style(f'border-color: {colors[entry["type"].lower()]["primary"]}'):
                                    with ui.row().classes('justify-between items-center'):
                                        ui.label(entry['date'].strftime('%B %d, %Y')).classes('font-bold')
                                        ui.label(f'{entry["type"].capitalize()} - Intensity: {entry["intensity"]}/10')
                                    if entry['text']:
                                        ui.label(entry['text']).classes('mt-2 text-gray-600')
                    else:
                        ui.label('No mood entries yet. Start tracking your moods!').classes('text-center text-gray-500')

                with ui.tab_panel('Mood Distribution'):
                    if mood_stats:
                        # Calculate mood distribution
                        mood_counts = {}
                        for entry in mood_stats:
                            mood_type = entry['type'].lower()
                            mood_counts[mood_type] = mood_counts.get(mood_type, 0) + 1

                        with ui.grid(columns=3).classes('gap-4'):
                            for mood_type, count in mood_counts.items():
                                with ui.card().classes('p-4').style(f'background: {colors[mood_type]["primary"]}22'):
                                    ui.label(f'{mood_type.capitalize()}').classes('font-bold')
                                    ui.label(f'{count} entries')
                                    percentage = count/len(mood_stats)*100
                                    ui.circular_progress(value=percentage, min=0, max=100, show_value=True)
                    else:
                        ui.label('No data available for mood distribution').classes('text-center text-gray-500')

                with ui.tab_panel('Tips & Recommendations'):
                    if mood_stats:
                        # Analyze recent moods
                        recent_moods = [m['type'].lower() for m in mood_stats[:5]]
                        
                        with ui.column().classes('gap-4'):
                            ui.label('Based on your recent mood patterns:').classes('text-xl font-bold')
                            
                            if 'anxiety' in recent_moods or 'fear' in recent_moods:
                                with ui.card().classes('p-4').style('background: #f0f7ff'):
                                    ui.label('Anxiety Management').classes('font-bold')
                                    ui.label('• Practice deep breathing exercises')
                                    ui.label('• Try mindfulness meditation')
                                    ui.label('• Consider talking to a counselor')
                            
                            if 'sadness' in recent_moods:
                                with ui.card().classes('p-4').style('background: #f3f0ff'):
                                    ui.label('Mood Lifting Activities').classes('font-bold')
                                    ui.label('• Engage in physical exercise')
                                    ui.label('• Connect with friends or family')
                                    ui.label('• Set small, achievable goals')
                            
                            if 'anger' in recent_moods:
                                with ui.card().classes('p-4').style('background: #fff0f0'):
                                    ui.label('Anger Management').classes('font-bold')
                                    ui.label('• Take time to cool down')
                                    ui.label('• Practice stress-relief techniques')
                                    ui.label('• Express feelings constructively')
                            
                            if 'joy' in recent_moods:
                                with ui.card().classes('p-4').style('background: #fffff0'):
                                    ui.label('Maintaining Positive Emotions').classes('font-bold')
                                    ui.label('• Share your happiness with others')
                                    ui.label('• Journal about positive experiences')
                                    ui.label('• Practice gratitude')
                    else:
                        ui.label('Start tracking your moods to get personalized recommendations').classes('text-center text-gray-500')

        # Add background styling
        ui.add_head_html('''
            <style>
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            
            .card {
                transition: all 0.3s ease;
            }
            
            .card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            </style>
        ''')

# 🔥 Memory to store entries per mood
entries = {
    'joy': [],
    'sadness': [],
    'anger': [],
    'fear': [],
    'disgust': [],
    'anxiety': []
}

# 🔥 Background images per mood
backgrounds = {
    'joy': "https://i.pinimg.com/736x/50/6e/84/506e84afe3accb975b597272f638658c.jpg",
    'sadness': "https://i.pinimg.com/736x/9c/24/1f/9c241fdce443dcb34323947596cd8e97.jpg",
    'anger': "https://i.pinimg.com/736x/f0/fb/9e/f0fb9ec074417216fbab47ce048cc083.jpg",
    'fear': "https://i.pinimg.com/736x/1d/78/07/1d78073e1059ffbb0169749e6f62936f.jpg",
    'anxiety': "https://i.pinimg.com/736x/08/b1/fd/08b1fd7d531e9a70c993213ec8fcc303.jpg",
    'disgust': "https://i.pinimg.com/736x/e0/c2/fa/e0c2fa8b6833e182afdcca648218ca23.jpg"
}

# 🔥 Colors for each mood
colors = {
    'joy': {
        'primary': '#FFD700',  # Golden
        'secondary': '#FFA500', # Orange
        'accent': '#FFFF00',    # Yellow
        'text': '#000000'       # Black
    },
    'sadness': {
        'primary': '#4169E1',   # Royal Blue
        'secondary': '#1E90FF',  # Dodger Blue
        'accent': '#87CEEB',    # Sky Blue
        'text': '#000000'       # black
    },
    'anger': {
        'primary': '#FF4500',   # Red Orange
        'secondary': '#FF6347',  # Tomato
        'accent': '#FF7F50',    # Coral
        'text': '#000000'       # black
    },
    'fear': {
        'primary': '#800080',   # Purple
        'secondary': '#9370DB',  # Medium Purple
        'accent': '#BA55D3',    # Medium Orchid
        'text': '#000000'       # black
    },
    'disgust': {
        'primary': '#32CD32',   # Lime Green
        'secondary': '#90EE90',  # Light Green
        'accent': '#98FB98',    # Pale Green
        'text': '#000000'       # Black
    },
    'anxiety': {
        'primary': '#FF69B4',   # Hot Pink
        'secondary': '#FF1493',  # Deep Pink
        'accent': '#FFB6C1',    # Light Pink
        'text': '#000000'       # Black
    }
}

# Global emoji mapping
emojis = {
    'joy': ['😊', '😃', '😄', '😁', '🤗', '😍', '🥰', '🌟', '✨', '🎉'],
    'sadness': ['🙁', '😔', '😢', '😥', '😪', '😓', '😖', '😩', '😫', '😭'],
    'anger': ['😠', '😡', '🤬', '💢', '👿', '😤', '😾', '💥', '🔥', '⚡'],
    'anxiety': ['😰', '😨', '😧', '😦', '😣', '😖', '😫', '😩', '🥺', '😵'],
    'fear': ['😨', '😰', '😱', '😖', '😣', '😫', '🥺', '😩', '😵', '💀'],
    'disgust': ['🤢', '🤮', '😖', '😫', '😤', '😠', '😡', '🤬', '👿', '😾']
}

def update_emoji(e):
    """Update the emoji based on the mood intensity value"""
    mood_name = e.sender.page.route[1:].split('_')[0].lower()  # Extract mood name from route
    intensity = e.value
    emoji_index = min(int(intensity) - 1, 9)  # Convert 1-10 to 0-9 index
    emoji_display.text = emojis[mood_name][emoji_index]

# Template function for mood pages
def create_mood_page(mood_name):
    @ui.page(f'/{mood_name.lower()}_log')
    def mood_page():
        create_nav_bar()  # Add navigation bar
        mood_colors = colors[mood_name.lower()]
        
        # Store emoji display reference
        global emoji_display
        
        # Add keyboard shortcut for generating new tips
        def on_key_press(e):
            if e.key == ' ':  # Space key
                update_tips(mood_intensity.value, force_new=True)
        
        ui.keyboard(on_key_press)
        
        with ui.column().classes('w-full min-h-screen p-8 gap-8 mt-16'):
            # Title with enhanced glow effect
            with ui.row().classes('justify-center w-full mb-8'):
                ui.label(f'{mood_name.capitalize()} Daily Log')\
                    .classes('text-6xl font-bold text-center cyber-text neon-glow')\
                    .style(f'''
                        font-family: "Orbitron", sans-serif;
                        color: {mood_colors['primary']};
                        text-shadow: 0 0 10px {mood_colors['secondary']},
                                   0 0 20px {mood_colors['accent']},
                                   0 0 30px {mood_colors['primary']};
                    ''')

            # Main content with improved visibility
            with ui.grid(columns=2).classes('gap-8 w-full'):
                # Left column - Enhanced Mood Entry
                with ui.card().classes('sticky-note max-w-sm cyber-note')\
                    .style(f'background: linear-gradient(135deg, {mood_colors["secondary"]}22, {mood_colors["accent"]}33);'):
                    ui.label('How are you feeling today?')\
                        .classes('text-lg font-bold mb-2')\
                        .style(f'color: {mood_colors["text"]}')
                    
                    input_box = ui.textarea(placeholder='Share your thoughts...')\
                        .classes('w-full mb-4 cyber-input floating-input')\
                        .style(f'''
                            height: 120px;
                            resize: none;
                            font-size: 14px;
                            line-height: 1.5;
                            background: rgba(255,255,255,0.95);
                            border: 2px solid {mood_colors["primary"]}66;
                        ''')

                    # Date/Time picker with modal
                    datetime_display = ui.label(datetime.now().strftime('%Y-%m-%d %H:%M'))\
                        .classes('text-sm mb-2')\
                        .style(f'color: {mood_colors["text"]}')


                    dialog = ui.dialog()  # Define the dialog
                    def show_datetime_modal():
                        with dialog, ui.card().classes('p-4 w-96'):
                            ui.label('Select Date and Time').classes('text-xl font-bold mb-4').style(f'color: {mood_colors["text"]}')
        
                            date_picker = ui.date(value=datetime.now().date()).classes('w-full mb-4').style(f'border-color: {mood_colors["primary"]}')
                            time_picker = ui.time(value=datetime.now().strftime("%H:%M")).classes('w-full mb-4').style(f'border-color: {mood_colors["primary"]}')

                            def update_datetime():
                                datetime_display.text = f"{date_picker.value} {time_picker.value}"
                                dialog.close()

                            ui.button('Confirm', on_click=update_datetime)\
                                .classes('w-full')\
                                .style(f'background: {mood_colors["primary"]}; color: {mood_colors["text"]};')

                        dialog.open()


                    ui.button('📅 Set Date & Time', on_click=show_datetime_modal)\
                        .classes('w-full mb-4 cyber-button')\
                        .style(f'''
                            background: {mood_colors["primary"]}22;
                            border: 2px solid {mood_colors["primary"]}44;
                            color: {mood_colors["text"]};
                        ''')

        
                    

            


                    # Mood intensity with enhanced visibility
                    ui.label(f'Rate your {mood_name} intensity:')\
                        .classes('mt-4')\
                        .style(f'color: {mood_colors["text"]}')
                    
                    with ui.row().classes('items-center justify-center w-full gap-4'):
                        emoji_display = ui.label('😐').classes('text-4xl cyber-emoji pulse-on-change')

                    def local_update_emoji(e):
                        intensity = e.value
                        emoji_index = min(int(intensity) - 1, 9)
                        emoji_display.text = emojis[mood_name.lower()][emoji_index]
                        # Update tips based on intensity
                        update_tips(intensity)

                    mood_intensity = ui.slider(min=1, max=10, value=5, on_change=local_update_emoji)\
                        .props('label-always')\
                        .classes('w-full cyber-slider')\
                        .style(f'''
                            background: linear-gradient(90deg,
                                {mood_colors["primary"]}33,
                                {mood_colors["secondary"]}66
                            );
                        ''')

                    def save_entry():
                        try:
                            timestamp = datetime_display.text
                            entry = {
                                'timestamp': timestamp,
                                'intensity': mood_intensity.value,
                                'text': input_box.value
                            }
                            
                            # Add to memory
                            entries[mood_name.lower()].append(entry)
                            
                            # Save to file
                            save_to_file()
                            
                            # Clear inputs and update UI
                            input_box.value = ''
                            mood_intensity.value = 5
                            ui.notify(f'Mood entry saved!', color=mood_colors["primary"])
                            display_entries()
                        except Exception as e:
                            ui.notify(f'Error saving entry: {str(e)}', color='red')

                    def save_to_file():
                        try:
                            # Create a data directory if it doesn't exist
                            os.makedirs('data', exist_ok=True)
                            
                            # Save entries to a JSON file
                            with open('data/mood_entries.json', 'w') as f:
                                json.dump(entries, f, indent=4)
                        except Exception as e:
                            ui.notify(f'Error saving to file: {str(e)}', color='red')

                    # Add this function to load saved entries when the app starts
                    def load_saved_entries():
                        try:
                            if os.path.exists('data/mood_entries.json'):
                                with open('data/mood_entries.json', 'r') as f:
                                    loaded_entries = json.load(f)
                                    entries.update(loaded_entries)
                        except Exception as e:
                            ui.notify(f'Error loading saved entries: {str(e)}', color='red')

                    # Call this when the page loads
                    load_saved_entries()

                    ui.button('Save Entry', on_click=save_entry)\
                        .classes('cyber-button hover-elevate mt-4')\
                        .style(f'''
                            background: {mood_colors["primary"]}22;
                            border: 2px solid {mood_colors["primary"]}44;
                            color: {mood_colors["text"]};
                            width: 100%;
                            padding: 10px;
                            border-radius: 8px;
                        ''')

                # Right column - Split into two sections
                with ui.column().classes('gap-8'):
                    # Previous Entries Section
                    with ui.card().classes('p-6 entries-container')\
                        .style(f'''
                            background: linear-gradient(135deg,
                                {mood_colors["primary"]}11,
                                {mood_colors["secondary"]}22
                            );
                            backdrop-filter: blur(10px);
                            border: 2px solid {mood_colors["primary"]}33;
                            border-radius: 15px;
                        '''):
                        ui.label('Previous Entries')\
                            .classes('text-xl font-bold mb-4')\
                            .style(f'color: {mood_colors["text"]}')
                        
                        entries_container = ui.row().classes('gap-4')
                        
                        def display_entries():
                            entries_container.clear()
                            with entries_container:
                                if not entries[mood_name.lower()]:
                                    ui.label('No entries yet')\
                                        .classes('text-center')\
                                        .style(f'color: {mood_colors["text"]}80')
                                else:
                                    for idx, entry in enumerate(reversed(entries[mood_name.lower()])):  # Add index for actions
                                        entry_index = len(entries[mood_name.lower()]) - idx - 1  # Get real index

                                        with ui.card().classes('entry-card p-4')\
                                            .style(f'''
                                                background: rgba(255,255,255,0.95);
                                                border: 2px solid {mood_colors["primary"]}33;
                                                border-radius: 10px;
                                                margin-bottom: 10px;
                                            '''):
                                            with ui.row().classes('justify-between items-center'):
                                                ui.label(entry['timestamp']).classes('text-sm').style(f'color: {mood_colors["text"]}80')
                                                ui.label(f'Intensity: {entry["intensity"]}/10').style(f'color: {mood_colors["text"]}')
                    
                                            if entry['text']:
                                                ui.label(entry['text']).classes('mt-2').style(f'color: {mood_colors["text"]}')
                    
                                                    # Edit & Delete Buttons
                                            with ui.row().classes('gap-4 mt-2'):
                                                ui.label('✏️')\
                                                    .classes('cursor-pointer text-sm hover:underline')\
                                                    .style(f'color: {mood_colors["primary"]};')\
                                                    .on('click', lambda idx=entry_index: edit_entry(idx))

                                                ui.label('🗑️ ')\
                                                    .classes('cursor-pointer text-sm hover:underline')\
                                                    .style('color: crimson;')\
                                                    .on('click', lambda idx=entry_index: delete_entry(idx))

                        def delete_entry(entry_idx):
                            entries[mood_name.lower()].pop(entry_idx)
                            display_entries()
                            ui.notify('Entry deleted.', color='red')

                        def edit_entry(entry_idx):
                            # Fill the input and intensity fields with selected entry data
                            input_box.value = entries[mood_name.lower()][entry_idx]['text']
                            mood_intensity.value = entries[mood_name.lower()][entry_idx]['intensity']
                            datetime_display.text = entries[mood_name.lower()][entry_idx]['timestamp']
                            # Remove the old one after editing
                            entries[mood_name.lower()].pop(entry_idx)
                            display_entries()
                            ui.notify('Edit the entry and save again.', color='blue')

                        display_entries()

                    # Auto-generated Tips Section
                    tips_container = ui.card().classes('p-6')\
                        .style(f'''
                            background: linear-gradient(135deg,
                                {mood_colors["primary"]}11,
                                {mood_colors["secondary"]}22
                            );
                            backdrop-filter: blur(10px);
                            border: 2px solid {mood_colors["primary"]}33;
                            border-radius: 15px;
                        ''')

                    def get_random_tips(mood_type, intensity):
                        all_tips = {
                            'joy': {
                                'high': [
                                    "Share your happiness with others!",
                                    "Journal about what made you so happy",
                                    "Take a photo to remember this moment",
                                    "Start a gratitude journal",
                                    "Plan something fun to maintain this energy",
                                    "Create something while feeling inspired",
                                    "Send a positive message to someone you care about",
                                    "Dance to your favorite upbeat song"
                                ],
                                'low': [
                                    "Try activities that boost your mood",
                                    "Connect with friends or family",
                                    "Practice gratitude",
                                    "Go for a walk in nature",
                                    "Listen to uplifting music",
                                    "Watch a funny video",
                                    "Do something kind for someone else",
                                    "Try a new hobby you've been interested in"
                                ]
                            },
                            'sadness': {
                                'high': [
                                    "Consider talking to a professional",
                                    "Practice deep breathing exercises",
                                    "Use grounding techniques",
                                    "Call a trusted friend or family member",
                                    "Write a letter expressing your feelings",
                                    "Take a warm bath or shower",
                                    "Create a comfort playlist",
                                    "Remember this feeling is temporary"
                                ],
                                'low': [
                                    "Try light exercise or stretching",
                                    "Listen to calming music",
                                    "Practice mindfulness",
                                    "Write down your feelings",
                                    "Watch a comforting movie",
                                    "Make your favorite tea",
                                    "Spend time in nature",
                                    "Do something creative"
                                ]
                            },
                            'anger': {
                                'high': [
                                    "Find a safe space to cool down",
                                    "Try progressive muscle relaxation",
                                    "Count backwards from 100",
                                    "Consider professional support",
                                    "Punch a pillow",
                                    "Write down what triggered you",
                                    "Take a timeout",
                                    "Use the 5-4-3-2-1 grounding technique"
                                ],
                                'low': [
                                    "Take deep breaths",
                                    "Go for a walk",
                                    "Listen to calming music",
                                    "Write down what's bothering you",
                                    "Practice mindful breathing",
                                    "Do some stretching",
                                    "Draw or doodle",
                                    "Talk to someone you trust"
                                ]
                            },
                            'anxiety': {
                                'high': [
                                    "Try the 4-7-8 breathing technique",
                                    "Use grounding exercises",
                                    "Call a supportive friend",
                                    "Write down your worries",
                                    "Practice progressive muscle relaxation",
                                    "Use a stress ball",
                                    "Try the 5-5-5 calming technique",
                                    "Consider professional guidance"
                                ],
                                'low': [
                                    "Do gentle stretching",
                                    "Practice mindfulness",
                                    "Listen to nature sounds",
                                    "Take a short walk",
                                    "Make a cup of herbal tea",
                                    "Color or draw",
                                    "Organize a small space",
                                    "Write in a journal"
                                ]
                            },
                            'fear': {
                                'high': [
                                    "Use the 5-4-3-2-1 senses exercise",
                                    "Call someone you trust",
                                    "Practice deep breathing",
                                    "Write down your fears",
                                    "Use positive affirmations",
                                    "Try visualization techniques",
                                    "Ground yourself in the present",
                                    "Consider professional support"
                                ],
                                'low': [
                                    "Do some light exercise",
                                    "Listen to calming music",
                                    "Write about your feelings",
                                    "Practice self-care",
                                    "Watch a comforting show",
                                    "Try a guided meditation",
                                    "Spend time with pets",
                                    "Read an engaging book"
                                ]
                            },
                            'disgust': {
                                'high': [
                                    "Remove yourself from the trigger",
                                    "Focus on pleasant sensations",
                                    "Practice acceptance techniques",
                                    "Use cleansing visualizations",
                                    "Try mindful breathing",
                                    "Change your environment",
                                    "Write about your feelings",
                                    "Consider professional guidance"
                                ],
                                'low': [
                                    "Focus on positive sensations",
                                    "Practice self-compassion",
                                    "Try grounding exercises",
                                    "Engage in a pleasant activity",
                                    "Listen to favorite music",
                                    "Take a refreshing shower",
                                    "Clean or organize something",
                                    "Connect with nature"
                                ]
                            }
                        }

                        mood_tips = all_tips.get(mood_type.lower(), all_tips['joy'])
                        intensity_category = 'high' if intensity >= 7 else 'low'
                        available_tips = mood_tips[intensity_category]
                        
                        import random
                        return random.sample(available_tips, min(4, len(available_tips)))

                    def update_tips(intensity, force_new=False):
                        tips_container.clear()
                        with tips_container:
                            with ui.row().classes('w-full justify-between items-center'):
                                ui.label('Suggested Tips')\
                                    .classes('text-xl font-bold mb-4')\
                                    .style(f'color: {mood_colors["text"]}')
                                ui.label('Press SPACE for new tips')\
                                    .classes('text-sm')\
                                    .style(f'color: {mood_colors["text"]}80')

                            tips = get_random_tips(mood_name, intensity)
                            
                            for tip in tips:
                                with ui.card().classes('tip-card p-4 mb-2')\
                                    .style(f'''
                                        background: rgba(255,255,255,0.95);
                                        border-left: 4px solid {mood_colors["primary"]};
                                    '''):
                                    ui.label(tip)\
                                        .style(f'color: {mood_colors["text"]}')

                    # Initial tips update
                    update_tips(5)

            ui.add_head_html(f'''
                <style>
                body {{
                    margin: 0;
                    padding: 0;
                    min-height: 100vh;
                    background-image: url("{backgrounds[mood_name.lower()]}");
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                    font-family: 'Orbitron', sans-serif;
                }}

                .tip-card {{
                    transition: all 0.3s ease;
                }}
                
                .tip-card:hover {{
                    transform: translateX(5px);
                }}
                
                .cyber-button {{
                    transition: all 0.3s ease;
                }}
                
                .cyber-button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px {mood_colors["primary"]}33;
                }}

                .entry-card {{
                    transition: all 0.3s ease;
                }}

                .entry-card:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px {mood_colors["secondary"]}33;
                }}

                .cyber-emoji {{
                    transition: all 0.3s ease;
                }}

                @keyframes pulseEmoji {{
                    0% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.2); }}
                    100% {{ transform: scale(1); }}
                }}

                .pulse-on-change {{
                    animation: pulseEmoji 0.5s ease;
                }}
                </style>
            ''')

# 🔥 Create all mood pages
for mood in entries.keys():
    create_mood_page(mood)

def analyze_mood(text):
    text = text.lower()
    if any(word in text for word in ['happy', 'excited', 'great', 'amazing']):
        return 'Happy'
    elif any(word in text for word in ['sad', 'depressed', 'unhappy', 'bad']):
        return 'Sad'
    elif any(word in text for word in ['anxious', 'nervous', 'stressed', 'worried']):
        return 'Anxious'
    elif any(word in text for word in ['okay', 'fine', 'normal', 'average']):
        return 'Neutral'
    else:
        return 'Neutral'  # Default if unknown

# Example usage
note = "I feel very stressed and tired today."
calculated_mood = analyze_mood(note)
print(calculated_mood)  # Output: Anxious

# Add global styles for navigation
ui.add_head_html('''
    <style>
    .nav-link {
        transition: all 0.3s ease;
        position: relative;
    }
    
    .nav-link::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 50%;
        width: 0;
        height: 2px;
        background: white;
        transition: all 0.3s ease;
        transform: translateX(-50%);
    }
    
    .nav-link:hover::after {
        width: 100%;
    }
    
    /* Ensure content doesn't hide behind fixed navbar */
    body {
        padding-top: 64px;
    }

    /* Quick action button hover effects */
    .quick-action {
        transition: all 0.3s ease;
    }
    
    .quick-action:hover {
        transform: scale(1.1);
        box-shadow: 0 0 15px rgba(255,255,255,0.2);
    }
    </style>
''')

def main():
    entry_manager = MoodEntryManager()
    
    # Create pages
    for mood in MOOD_CONFIG:
        MoodPageFactory.create_page(mood, entry_manager)
    
   

if __name__ == "__main__":
    main()
  
ui.run()