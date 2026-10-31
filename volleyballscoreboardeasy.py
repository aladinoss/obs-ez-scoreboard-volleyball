import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
from flask import Flask, render_template_string, request, redirect, url_for, jsonify

# Initialize Flask App for Remote Control
web_app = Flask(__name__)
scoreboard_ref = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Volleyball Scoreboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; background: #121212; color: #fff; margin: 0; padding: 6px; text-align: center; }
        .team-row { background: #1e1e1e; border-radius: 6px; padding: 6px 10px; margin: 6px auto; max-width: 450px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 4px rgba(0,0,0,0.4); }
        .team-info { text-align: left; flex-grow: 1; margin-left: 10px; }
        .team-name { font-size: 14px; font-weight: bold; color: #64b5f6; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 160px; }
        .team-2 .team-name { color: #ff8a65; }
        .score-display { font-size: 26px; font-weight: bold; margin: 0 5px; min-width: 35px; text-align: right; }
        .sets-display { font-size: 11px; color: #aaa; }
        .btn-group { display: flex; gap: 3px; }
        button { padding: 6px 10px; font-size: 13px; font-weight: bold; border: none; border-radius: 4px; cursor: pointer; color: white; }
        .btn-plus { background: #2e7d32; }
        .btn-plus:active { background: #1b5e20; }
        .btn-minus { background: #c62828; }
        .btn-minus:active { background: #b71c1c; }
        .btn-action { background: #b71c1c; padding: 8px; font-size: 12px; margin-top: 4px; width: 100%; max-width: 450px; border-radius: 4px; }
    </style>
</head>
<body>
    <!-- Team 1 Row -->
    <div class="team-row">
        <div class="btn-group">
            <form action="/t1_sub" method="post"><button class="btn-minus">-</button></form>
            <form action="/t1_add" method="post"><button class="btn-plus">+</button></form>
        </div>
        <div class="team-info">
            <div id="t1_name_lbl" class="team-name">{{ t1_name }}</div>
            <div class="sets-display">Sets: <span id="t1_sets_lbl">{{ t1_sets }}</span></div>
        </div>
        <div id="t1_score_lbl" class="score-display">{{ t1_score }}</div>
    </div>

    <!-- Team 2 Row -->
    <div class="team-row team-2">
        <div class="btn-group">
            <form action="/t2_sub" method="post"><button class="btn-minus">-</button></form>
            <form action="/t2_add" method="post"><button class="btn-plus">+</button></form>
        </div>
        <div class="team-info">
            <div id="t2_name_lbl" class="team-name">{{ t2_name }}</div>
            <div class="sets-display">Sets: <span id="t2_sets_lbl">{{ t2_sets }}</span></div>
        </div>
        <div id="t2_score_lbl" class="score-display">{{ t2_score }}</div>
    </div>

    <!-- Reset Score Only -->
    <div style="max-width: 450px; margin: 0 auto;">
        <form action="/reset_set" method="post">
            <button class="btn-action">Reset Set Score (0-0)</button>
        </form>
    </div>

    <script>
        // Live auto-sync polls every 1 second
        setInterval(async () => {
            try {
                let response = await fetch('/api/status');
                let data = await response.json();
                document.getElementById('t1_name_lbl').innerText = data.t1_name;
                document.getElementById('t2_name_lbl').innerText = data.t2_name;
                document.getElementById('t1_score_lbl').innerText = data.t1_score;
                document.getElementById('t2_score_lbl').innerText = data.t2_score;
                document.getElementById('t1_sets_lbl').innerText = data.t1_sets;
                document.getElementById('t2_sets_lbl').innerText = data.t2_sets;
            } catch (e) {
                console.log("Sync error:", e);
            }
        }, 1000);
    </script>
</body>
</html>
"""

@web_app.route('/')
def index():
    if scoreboard_ref:
        return render_template_string(HTML_TEMPLATE, 
            t1_name=scoreboard_ref.team1_name.get(),
            t2_name=scoreboard_ref.team2_name.get(),
            t1_score=scoreboard_ref.team1_score.get(),
            t2_score=scoreboard_ref.team2_score.get(),
            t1_sets=scoreboard_ref.team1_sets.get(),
            t2_sets=scoreboard_ref.team2_sets.get()
        )
    return "Server initializing..."

@web_app.route('/api/status')
def api_status():
    if scoreboard_ref:
        return jsonify({
            't1_name': scoreboard_ref.team1_name.get(),
            't2_name': scoreboard_ref.team2_name.get(),
            't1_score': scoreboard_ref.team1_score.get(),
            't2_score': scoreboard_ref.team2_score.get(),
            't1_sets': scoreboard_ref.team1_sets.get(),
            't2_sets': scoreboard_ref.team2_sets.get()
        })
    return jsonify({})

@web_app.route('/t1_add', methods=['POST'])
def web_t1_add():
    if scoreboard_ref: scoreboard_ref.root.after(0, scoreboard_ref.t1_add)
    return redirect(url_for('index'))

@web_app.route('/t1_sub', methods=['POST'])
def web_t1_sub():
    if scoreboard_ref: scoreboard_ref.root.after(0, scoreboard_ref.t1_sub)
    return redirect(url_for('index'))

@web_app.route('/t2_add', methods=['POST'])
def web_t2_add():
    if scoreboard_ref: scoreboard_ref.root.after(0, scoreboard_ref.t2_add)
    return redirect(url_for('index'))

@web_app.route('/t2_sub', methods=['POST'])
def web_t2_sub():
    if scoreboard_ref: scoreboard_ref.root.after(0, scoreboard_ref.t2_sub)
    return redirect(url_for('index'))

@web_app.route('/reset_set', methods=['POST'])
def web_reset():
    if scoreboard_ref: scoreboard_ref.root.after(0, scoreboard_ref.reset_set)
    return redirect(url_for('index'))


class VolleyballScoreboardApp:
    def __init__(self, root):
        global scoreboard_ref
        scoreboard_ref = self

        self.root = root
        self.root.title("Volleyball Scoreboard Control Panel")
        self.root.geometry("600x580")
        self.root.resizable(False, False)

        self.output_dir = os.path.join(os.getcwd(), "scoreboard_data")
        os.makedirs(self.output_dir, exist_ok=True)

        self.team1_name = tk.StringVar(value="TEAM 1")
        self.team2_name = tk.StringVar(value="TEAM 2")
        self.team1_score = tk.IntVar(value=0)
        self.team2_score = tk.IntVar(value=0)
        self.team1_sets = tk.IntVar(value=0)
        self.team2_sets = tk.IntVar(value=0)

        self.hotkeys = {
            "t1_plus": "F5",
            "t1_minus": "F6",
            "t2_plus": "F7",
            "t2_minus": "F8",
            "swap": "F9",
            "reset_scores": "F10"
        }

        self.setup_ui()
        self.update_all_files()
        self.bind_global_hotkeys()

        # Start Flask web server in background
        threading.Thread(target=lambda: web_app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False), daemon=True).start()

    def setup_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        control_frame = ttk.Frame(notebook)
        notebook.add(control_frame, text="Score Control")

        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="Hotkey Settings")

        self.build_control_tab(control_frame)
        self.build_settings_tab(settings_frame)

    def build_control_tab(self, frame):
        names_frame = ttk.LabelFrame(frame, text="Team Names", padding=10)
        names_frame.pack(fill="x", padx=10, pady=5)

        ttk.Entry(names_frame, textvariable=self.team1_name, font=("Arial", 12), width=15).grid(row=0, column=0, padx=5)
        ttk.Label(names_frame, text="VS", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10)
        ttk.Entry(names_frame, textvariable=self.team2_name, font=("Arial", 12), width=15).grid(row=0, column=2, padx=5)

        self.team1_name.trace_add("write", lambda *args: self.write_file("team1_name.txt", self.team1_name.get()))
        self.team2_name.trace_add("write", lambda *args: self.write_file("team2_name.txt", self.team2_name.get()))

        score_frame = ttk.LabelFrame(frame, text="Match Scores & Remote Info", padding=10)
        score_frame.pack(fill="both", expand=True, padx=10, pady=5)

        info_lbl = ttk.Label(score_frame, text="📱 Tablet Remote Link: http://[YOUR_PC_IP]:5000", foreground="#2b5c8f", font=("Arial", 10, "bold"), justify="center")
        info_lbl.pack(pady=(0, 10))

        teams_container = ttk.Frame(score_frame)
        teams_container.pack()

        # Team 1 Controls
        t1_box = ttk.Frame(teams_container)
        t1_box.grid(row=0, column=0, padx=15)
        ttk.Label(t1_box, textvariable=self.team1_name, font=("Arial", 12, "bold")).pack()
        ttk.Label(t1_box, textvariable=self.team1_score, font=("Arial", 36, "bold"), foreground="#2b5c8f").pack()
        
        btn_box1 = ttk.Frame(t1_box)
        btn_box1.pack()
        ttk.Button(btn_box1, text="+1 (F5)", command=self.t1_add).pack(side="left", padx=2)
        ttk.Button(btn_box1, text="-1 (F6)", command=self.t1_sub).pack(side="left", padx=2)

        ttk.Label(t1_box, text="Sets:").pack(pady=(5, 0))
        set_box1 = ttk.Frame(t1_box)
        set_box1.pack()
        ttk.Button(set_box1, text="-", width=2, command=lambda: self.change_sets(1, -1)).pack(side="left")
        ttk.Label(set_box1, textvariable=self.team1_sets, font=("Arial", 12, "bold")).pack(side="left", padx=5)
        ttk.Button(set_box1, text="+", width=2, command=lambda: self.change_sets(1, 1)).pack(side="left")

        # Team 2 Controls
        t2_box = ttk.Frame(teams_container)
        t2_box.grid(row=0, column=1, padx=15)
        ttk.Label(t2_box, textvariable=self.team2_name, font=("Arial", 12, "bold")).pack()
        ttk.Label(t2_box, textvariable=self.team2_score, font=("Arial", 36, "bold"), foreground="#bf360c").pack()

        btn_box2 = ttk.Frame(t2_box)
        btn_box2.pack()
        ttk.Button(btn_box2, text="+1 (F7)", command=self.t2_add).pack(side="left", padx=2)
        ttk.Button(btn_box2, text="-1 (F8)", command=self.t2_sub).pack(side="left", padx=2)

        ttk.Label(t2_box, text="Sets:").pack(pady=(5, 0))
        set_box2 = ttk.Frame(t2_box)
        set_box2.pack()
        ttk.Button(set_box2, text="-", width=2, command=lambda: self.change_sets(2, -1)).pack(side="left")
        ttk.Label(set_box2, textvariable=self.team2_sets, font=("Arial", 12, "bold")).pack(side="left", padx=5)
        ttk.Button(set_box2, text="+", width=2, command=lambda: self.change_sets(2, 1)).pack(side="left")

        # Action Buttons
        actions_frame = ttk.Frame(frame)
        actions_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(actions_frame, text="Swap Sides (F9)", command=self.swap_sides).pack(side="left", expand=True, fill="x", padx=3)
        ttk.Button(actions_frame, text="Reset Set (F10)", command=self.reset_set).pack(side="left", expand=True, fill="x", padx=3)
        ttk.Button(actions_frame, text="Reset Match", command=self.reset_match).pack(side="left", expand=True, fill="x", padx=3)

    def build_settings_tab(self, frame):
        lbl = ttk.Label(frame, text="Configure Global Hotkeys", font=("Arial", 11, "bold"))
        lbl.pack(pady=10)

        self.hotkey_entries = {}
        labels = {
            "t1_plus": "Team 1 (+1 Point):",
            "t1_minus": "Team 1 (-1 Point):",
            "t2_plus": "Team 2 (+1 Point):",
            "t2_minus": "Team 2 (-1 Point):",
            "swap": "Swap Sides:",
            "reset_scores": "Reset Set Scores:"
        }

        form = ttk.Frame(frame, padding=20)
        form.pack()

        row = 0
        for key, text in labels.items():
            ttk.Label(form, text=text, font=("Arial", 10)).grid(row=row, column=0, sticky="e", pady=5, padx=5)
            entry = ttk.Entry(form, width=10)
            entry.insert(0, self.hotkeys[key])
            entry.grid(row=row, column=1, sticky="w", pady=5, padx=5)
            self.hotkey_entries[key] = entry
            row += 1

        ttk.Button(frame, text="Apply New Hotkeys", command=self.apply_new_hotkeys).pack(pady=15)

    def t1_add(self):
        self.team1_score.set(self.team1_score.get() + 1)
        self.write_file("team1_score.txt", str(self.team1_score.get()))

    def t1_sub(self):
        if self.team1_score.get() > 0:
            self.team1_score.set(self.team1_score.get() - 1)
            self.write_file("team1_score.txt", str(self.team1_score.get()))

    def t2_add(self):
        self.team2_score.set(self.team2_score.get() + 1)
        self.write_file("team2_score.txt", str(self.team2_score.get()))

    def t2_sub(self):
        if self.team2_score.get() > 0:
            self.team2_score.set(self.team2_score.get() - 1)
            self.write_file("team2_score.txt", str(self.team2_score.get()))

    def change_sets(self, team, delta):
        if team == 1:
            val = max(0, self.team1_sets.get() + delta)
            self.team1_sets.set(val)
            self.write_file("team1_sets.txt", str(val))
        else:
            val = max(0, self.team2_sets.get() + delta)
            self.team2_sets.set(val)
            self.write_file("team2_sets.txt", str(val))

    def swap_sides(self):
        n1, n2 = self.team1_name.get(), self.team2_name.get()
        self.team1_name.set(n2)
        self.team2_name.set(n1)

        s1, s2 = self.team1_score.get(), self.team2_score.get()
        self.team1_score.set(s2)
        self.team2_score.set(s1)

        set1, set2 = self.team1_sets.get(), self.team2_sets.get()
        self.team1_sets.set(set2)
        self.team2_sets.set(set1)

        self.update_all_files()

    def reset_set(self):
        self.team1_score.set(0)
        self.team2_score.set(0)
        self.write_file("team1_score.txt", "0")
        self.write_file("team2_score.txt", "0")

    def reset_match(self):
        self.reset_set()
        self.team1_sets.set(0)
        self.team2_sets.set(0)
        self.write_file("team1_sets.txt", "0")
        self.write_file("team2_sets.txt", "0")

    def write_file(self, filename, content):
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def update_all_files(self):
        self.write_file("team1_name.txt", self.team1_name.get())
        self.write_file("team2_name.txt", self.team2_name.get())
        self.write_file("team1_score.txt", str(self.team1_score.get()))
        self.write_file("team2_score.txt", str(self.team2_score.get()))
        self.write_file("team1_sets.txt", str(self.team1_sets.get()))
        self.write_file("team2_sets.txt", str(self.team2_sets.get()))

    def bind_global_hotkeys(self):
        try:
            keyboard.unhook_all()
            keyboard.add_hotkey(self.hotkeys["t1_plus"], lambda: self.root.after(0, self.t1_add))
            keyboard.add_hotkey(self.hotkeys["t1_minus"], lambda: self.root.after(0, self.t1_sub))
            keyboard.add_hotkey(self.hotkeys["t2_plus"], lambda: self.root.after(0, self.t2_add))
            keyboard.add_hotkey(self.hotkeys["t2_minus"], lambda: self.root.after(0, self.t2_sub))
            keyboard.add_hotkey(self.hotkeys["swap"], lambda: self.root.after(0, self.swap_sides))
            keyboard.add_hotkey(self.hotkeys["reset_scores"], lambda: self.root.after(0, self.reset_set))
        except Exception as e:
            messagebox.showerror("Hotkey Error", f"Failed to register hotkeys: {e}")

    def apply_new_hotkeys(self):
        for key, entry in self.hotkey_entries.items():
            self.hotkeys[key] = entry.get().strip()
        self.bind_global_hotkeys()
        messagebox.showinfo("Success", "Hotkeys updated successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = VolleyballScoreboardApp(root)
    root.mainloop()