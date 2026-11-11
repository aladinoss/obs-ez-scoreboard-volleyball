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



Here is an expanded section you can add to your documentation or use to set up your OBS scene. It covers step-by-step instructions on configuring OBS to read from your local text files and how to layer them neatly over a custom transparent background graphic.

---

### 🎨 OBS Visual Setup: Background PNG + Dynamic Text Overlays

To get a professional broadcast look, you can use a nice scoreboard graphic template (a transparent PNG) as your background, and place your dynamic text fields directly on top of it.

#### **Step 1: Add Your Scoreboard Background Image**

1. In OBS Studio, go to your **Sources** panel and click **`+`** $\rightarrow$ **Image**.
2. Name it something like `Scoreboard Background` and click OK.
3. Click **Browse** and select your custom transparent scoreboard image (e.g., a `.png` file with a sleek background banner for the scores and team names).
4. Resize and position the image wherever you want it to appear on your stream (e.g., top-center or bottom-center).

#### **Step 2: Configure OBS Text Sources (Reading from Files)**

For each piece of data (Team Names, Scores, Sets), you need to create a dedicated text source:

1. Click **`+`** in the **Sources** panel $\rightarrow$ **Text (GDI+)** (or *Text (FreeType2)* on Mac/Linux).
2. Name it clearly (e.g., `Team1_Score_Text`).
3. In the properties window:
* **Check the box** for **"Read from file"**.
* Click **Browse** and select the matching text file from your app's folder (e.g., `scoreboard_data/team1_score.txt`).
* Choose your preferred font, size, and text color so it stands out clearly against your background graphic.
* Set text alignment (e.g., Center).


4. Click **OK**. Repeat this for `team2_score.txt`, `team1_name.txt`, `team2_name.txt`, etc.

#### **Step 3: Layer Text Boxes on Top of the Background**

1. In the **Sources** panel, make sure your text sources are listed **directly above** the `Scoreboard Background` image layer. *(In OBS, items higher up in the list appear on top of items below them).*
2. Drag and drop each text box directly onto its corresponding placeholder slot on your background PNG (e.g., place `Team1_Score_Text` right over the score box area on your graphic).

#### **Step 4: Group Your Sources (Pro Tip)**

To make moving or resizing your scoreboard easier later:

1. Hold down the `Ctrl` key and click on your background image and all your text sources in the Sources list to select them all together.
2. Right-click your selection and choose **Group Selected Items**.
3. Name the group `Scoreboard`. Now you can move, resize, or hide/show the entire scoreboard layout as a single unit without messing up individual text alignments!

---

### 🔄 How the Auto-Update Workflow Works

Once configured, your live stream updates completely hands-free:

1. **You tap a button** on your tablet's web remote (or press `F5`–`F8` on your PC keyboard).
2. **The Python script** instantly captures the action and overwrites the local `.txt` files inside the `scoreboard_data/` folder.
3. **OBS Studio** constantly monitors these text files and instantly re-reads them the millisecond they change.
4. **Your live stream updates automatically** on screen—allowing you to focus entirely on watching the match on YouTube and keeping the score up to date in real time!
