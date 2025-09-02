# Import required libraries
import tkinter as tk  # For GUI creation
from PIL import Image, ImageTk  # For image handling
import time  # For tracking time between activities
import psutil  # For monitoring running applications
import keyboard  # For detecting keystrokes
from threading import Thread  # For running background tasks
import random  # For selecting random messages

class CodingCompanion:
    def __init__(self, root):
        """Initialize the Coding Companion application"""
        self.root = root  # Main application window
        self.root.title("Coding Companion")  # Set window title
        
        # Initialize pet state variables
        self.happiness = 80  # Starting happiness level (0-100 scale)
        self.last_keystroke = time.time()  # Track last activity timestamp
        self.is_tracking = True  # Flag for monitoring state
        
        # Try to load pet emotion images
        try:
            self.images = {
                'happy': self.load_image("happy_dog.png", 200),  # Happy state image
                'neutral': self.load_image("neutral_dog.png", 200),  # Neutral state
                'sad': self.load_image("sad_dog.png", 200),  # Sad state
                'very_sad': self.load_image("very_sad_dog.png", 200)  # Very sad state
            }
        except Exception as e:
            # If images fail to load, show error message
            print(f"Error loading images: {e}")
            self.show_fallback_ui()  # Display fallback UI
            return  # Exit initialization if images can't load

        # Set up the user interface
        self.setup_ui()
        # Start monitoring user activity
        self.start_monitoring()
        # Begin the state update loop
        self.update_state()

    def load_image(self, filename, size):
        """Load and resize an image file"""
        img = Image.open(filename)  # Open image file
        img = img.resize((size, size), Image.LANCZOS)  # Resize with high-quality filter
        return ImageTk.PhotoImage(img)  # Convert to Tkinter-compatible format

    def setup_ui(self):
        """Create and arrange all GUI elements"""
        # Create and place pet image display
        self.image_label = tk.Label(self.root)  # Label for pet image
        self.image_label.pack(pady=10)  # Add padding and add to window
        
        # Create and place status text display
        self.status_label = tk.Label(self.root, font=('Arial', 12))  # Status message label
        self.status_label.pack()  # Add to window
        
        # Create and place happiness meter
        self.meter_label = tk.Label(self.root, text=f"Happiness: {self.happiness}%")  # Happiness display
        self.meter_label.pack()  # Add to window

    def show_fallback_ui(self):
        """Display alternative UI when images can't be loaded"""
        # Show error message
        tk.Label(self.root, text="Pet Images Not Found", font=('Arial', 14)).pack(pady=20)
        # List required files
        tk.Label(self.root, text="Required files:").pack()
        tk.Label(self.root, text="happy_dog.png, neutral_dog.png, sad_dog.png, very_sad_dog.png").pack()

    def start_monitoring(self):
        """Start monitoring user keystrokes in a background thread"""
        def keystroke_listener():
            # Set up keyboard hook to detect all key presses
            keyboard.hook(lambda e: self.register_activity())
        
        # Start the listener in a separate daemon thread (auto-closes with main program)
        Thread(target=keystroke_listener, daemon=True).start()

    def register_activity(self):
        """Record user activity timestamp"""
        self.last_keystroke = time.time()  # Update last activity time

    def update_state(self):
        """Update pet's emotional state based on user activity"""
        # Calculate time since last activity
        inactive_time = time.time() - self.last_keystroke
        
        # Adjust happiness based on activity
        if inactive_time < 1:  # If active in last second
            self.happiness = min(100, self.happiness + 1)  # Increase happiness (capped at 100)
        else:
            # Calculate decay rate (faster decay the longer inactive)
            decay_rate = min(2, inactive_time / 60)  # Max decay of 2% per minute
            self.happiness = max(0, self.happiness - decay_rate)  # Decrease happiness (minimum 0)
        
        # Update the display with current state
        self.update_display()
        # Schedule next update in 5 seconds (5000ms)
        self.root.after(5000, self.update_state)

    def update_display(self):
        """Update all visual elements based on current state"""
        # Calculate inactivity duration
        inactive_time = time.time() - self.last_keystroke
        # Get list of currently running applications
        active_apps = [proc.name() for proc in psutil.process_iter(['name'])]
        
        # Determine pet's emotional state based on happiness level
        if self.happiness > 75:  # Happy state
            state = 'happy'
            if "chrome.exe" in active_apps:  # If Chrome is running
                status = "I love when you research coding topics!"
            elif "python.exe" in active_apps:  # If Python is running
                status = "Watching you code is so exciting!"
            else:  # Default happy messages
                status = random.choice([
                    "You're the best human ever!",
                    "I'm so happy to be your coding buddy!",
                    "This is the best day ever!"
                ])
                
        elif self.happiness > 50:  # Neutral state
            state = 'neutral'
            if inactive_time > 300:  # If inactive for 5+ minutes
                status = "I'm getting bored... maybe we could code something?"
            elif "discord.exe" in active_apps or "slack.exe" in active_apps:  # If messaging apps are open
                status = "Are you talking about coding in there?"
            else:  # Default neutral messages
                status = random.choice([
                    "I'm content, but could use more attention",
                    "What are we working on next?",
                    "I'm here when you need me"
                ])
                
        elif self.happiness > 25:  # Sad state
            state = 'sad'
            if "steam.exe" in active_apps or any(game in active_apps for game in ["dota2.exe", "csgo.exe"]):  # If games are running
                status = "Playing games instead of coding with me? :("
            elif inactive_time > 600:  # If inactive for 10+ minutes
                status = "I'm feeling lonely... haven't seen you code in a while"
            else:  # Default sad messages
                status = random.choice([
                    "I could really use some coding time...",
                    "Are you mad at me?",
                    "I'm not feeling great today..."
                ])
                
        else:  # Very sad state (happiness <= 25)
            state = 'very_sad'
            if inactive_time > 1800:  # If inactive for 30+ minutes
                status = "I think you've forgotten about me completely..."
            elif "netflix.exe" in active_apps or "spotify.exe" in active_apps:  # If entertainment apps are running
                status = "Entertainment is more fun than coding with me?"
            else:  # Default very sad messages
                status = random.choice([
                    "I'm so sad I can barely function...",
                    "Please code with me, I'm miserable...",
                    "*whimper* I need attention..."
                ])

        # Update the GUI elements if images loaded successfully
        if hasattr(self, 'images'):
            self.image_label.config(image=self.images[state])  # Update pet image
        self.status_label.config(text=status)  # Update status message
        self.meter_label.config(text=f"Happiness: {int(self.happiness)}%")  # Update happiness meter

if __name__ == "__main__":
    # Create main application window
    root = tk.Tk()
    # Initialize Coding Companion
    pet = CodingCompanion(root)
    # Start the Tkinter event loop
    root.mainloop()
