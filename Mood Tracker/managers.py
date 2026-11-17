from collections import defaultdict
from datetime import datetime

class MoodEntryManager:
    def __init__(self):
        self.entries = defaultdict(list)
    
    def add_entry(self, mood_type: str, intensity: int, text: str):
        entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'intensity': intensity,
            'text': text
        }
        self.entries[mood_type].append(entry)
        return entry 