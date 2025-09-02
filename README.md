The Virtual Coding Companion is an interactive AI pet designed to support developers 
directly within their workflow. This playful pug lives in a compact GUI window, offering real
time emotional feedback based on your coding activity. More than just a cute distraction, 
it serves as a productivity partner—encouraging focus, rewarding progress, and adding 
warmth to the development process. 

This project aims to 
✓ Boost productivity 
✓ Combat isolation 
✓ Intelligent Monitor keystrokes and application usage to assess engagement 
✓ Context-Aware Motivate user by sending messages based on coding environment, distractions, 
extended breaks

Core stack 
• Python - primary programming language for application logic and integration

GUI Development 
• Tkinter Python Library – creating the GUI box, build interactive desktop apps with a graphical 
interface 
• PIL (Pillow) (Image, ImageTk) - handles image loading/resizing for the pet’s emotional states 

Activity Monitoring 
• Psutil – detects active apps (Chrome, Discord etc.) to customize pet’s reactions 
• Keyboard - listens for keystrokes to measure user activity 
• Time - tracks inactivity and manages happiness decay over time

Performance and Dynamic Content 
• Threading (Thread) - runs keystroke tracking in the background without blocking the GUI, critical 
for multitasking in applications 
• Random – randomize pet messages for variety

The AI System 
1. Emotion Modeling & State Management 
• Dynamic Happiness Algorithm: The pet’s mood isn’t random—it reacts to your behavior using a 
decay/reward system: 
o Rewards coding: Happiness increases with keystrokes (direct correlation to productivity). 
o Punishes inactivity: Happiness decays exponentially over time (simulates "neglect"). 
o 4 Emotional States: 
− Happy (75–100%): Active coding → cheerful reactions. 
− Neutral (50–75%): Mild inactivity → gentle reminders. 
− Sad (25–50%): Long breaks → pleading messages. 
− Very Sad (0–25%): Abandonment → dramatic despair. 
2. Context-Aware Intelligence 
• Process Monitoring (via psutil): Detects apps to infer user intent: 
o Positive triggers: 
− vscode.exe, python.exe → "Keep coding! I love this! 
o Negative triggers: 
− steam.exe, discord.exe → "Are we playing instead of coding? :(" 
o Neutral triggers: 
− chrome.exe → "Researching something cool?" 
3. Behavioral Adaptation 
• Personalized Messaging: Uses random to select from mood-appropriate messages, avoiding 
repetition. 
• Time-Based Escalation: 
o Short breaks → "Missed you!" 
+30 min inactivity → "Whimpers… Where are you?"
