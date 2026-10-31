🏐 OBS Volleyball Scoreboard & Mobile Remote (Python)
A lightweight, free, and easy-to-use tool to manage and broadcast volleyball match scores live on OBS Studio. It can be controlled via global PC keyboard shortcuts or wirelessly using a compact web remote on a tablet or smartphone.

🎯 Use Case
Perfect for amateur sports broadcasters (local clubs, school tournaments, or regional leagues) streaming to YouTube or Twitch.

The Problem: Manually updating text sources inside OBS during a live match is cumbersome, and paid cloud solutions or complex plugins are often overkill.

The Solution: A lightweight Python application that instantly writes scores to local text files for OBS. It can be controlled either via hotkeys (F5–F8) on your broadcast PC or from a tablet connected to the same Wi-Fi—allowing you to watch your live stream's return feed while updating scores on the fly.

✨ Key Features
📁 Native OBS Integration: Updates local .txt files in real-time (fully compatible with OBS Text sources using the "Read from file" feature).

⌨️ Global Keyboard Hotkeys: Fully customizable bindings (default: F5 to F8 for points) that work even when OBS is running in the background.

📱 Compact Tablet Web Remote: A streamlined mobile interface designed for split-screen tablet use, featuring compact +/- buttons right next to team names and auto-syncing in real time.

🔒 Local Network Security: Runs entirely on your private local Wi-Fi network with zero exposure to the public internet.

🛠️ Installation & Setup Guide
1. Prerequisites
Make sure Python 3 is installed on your broadcasting PC.

Open your terminal or command prompt and install the required dependencies:

Bash
pip install keyboard flask
(Note: Windows users should run their command prompt/terminal as Administrator so global hotkeys can register properly).

2. Running the Application
Save the Python script (e.g., volleyball_scoreboard.py) on your PC.

Run the script:

Bash
python volleyball_scoreboard.py
A desktop control panel will open, and a scoreboard_data/ folder will be created automatically in the same directory.

3. Setting Up OBS Studio
For each element you want to display on your overlay:

In OBS, add a Text (GDI+) or Text (FreeType2) source.

Check the box for "Read from file".

Click Browse and select the corresponding text file inside the scoreboard_data/ folder:

team1_name.txt / team2_name.txt (Team names)

team1_score.txt / team2_score.txt (Current set scores)

team1_sets.txt / team2_sets.txt (Sets won)

Position your text sources over your scoreboard graphic template.

4. Using the Tablet Remote
Connect your tablet to the same Wi-Fi network as your broadcast PC.

On your PC, find your local IP address (open Command Prompt on Windows, type ipconfig, and look for your IPv4 Address, e.g., 192.168.1.15).

Open your tablet's web browser and go to:http://[YOUR_PC_IP]:5000 (Example: [http://192.168.1.15:5000](http://192.168.1.15:5000))

You will see a clean, compact control interface to manage scores instantly while watching your broadcast!

⌨️ Default Keyboard Shortcuts (Fully customizable in the app's settings tab):
F5: Team 1 Point (+1)

F6: Team 1 Minus (-1)

F7: Team 2 Point (+1)

F8: Team 2 Minus (-1)

F9: Swap Sides

F10: Reset Current Set Score (0-0)
