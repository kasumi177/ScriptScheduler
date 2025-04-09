import tkinter as tk
from tkinter import ttk, filedialog
import time
import subprocess
import threading
import os
import json
import psutil
import platform

class ScriptScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Script Scheduler")
        self.scripts = []
        self.time_in_seconds = 0
        self.running = False
        self.config_file = "scheduler_config.json"
        self.processes = []
        self.timer_thread = None
        
        self.load_config()
        
        tk.Label(root, text="Stunden:").grid(row=0, column=0, padx=5, pady=5)
        self.hours = tk.Entry(root, width=5)
        self.hours.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(root, text="Minuten:").grid(row=1, column=0, padx=5, pady=5)
        self.minutes = tk.Entry(root, width=5)
        self.minutes.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(root, text="Sekunden:").grid(row=2, column=0, padx=5, pady=5)
        self.seconds = tk.Entry(root, width=5)
        self.seconds.grid(row=2, column=1, padx=5, pady=5)
        
        self.set_button = tk.Button(root, text="Zeit speichern", command=self.save_time)
        self.set_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        tk.Label(root, text="Python Script Pfad:").grid(row=4, column=0, padx=5, pady=5)
        self.path_entry = tk.Entry(root, width=30)
        self.path_entry.grid(row=4, column=1, padx=5, pady=5)
        
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=4, column=2, padx=5, pady=5)
        
        self.add_button = tk.Button(root, text="Hinzufügen", command=self.add_script)
        self.add_button.grid(row=5, column=1, pady=5)
        
        self.script_list = tk.Listbox(root, height=10, width=40)
        self.script_list.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        
        self.delete_button = tk.Button(root, text="Entfernen", command=self.delete_script)
        self.delete_button.grid(row=7, column=0, pady=5)
        
        self.start_button = tk.Button(root, text="Start", command=self.start_scripts)
        self.start_button.grid(row=7, column=1, pady=5)
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_scripts)
        self.stop_button.grid(row=7, column=2, pady=5)
        
        tk.Label(root, text="Zeit bis Neustart:").grid(row=8, column=0, padx=5, pady=5)
        self.restart_timer_label = tk.Label(root, text="Nicht gestartet")
        self.restart_timer_label.grid(row=8, column=1, padx=5, pady=5)
        
        self.edit_button = tk.Button(root, text="Start-Optionen bearbeiten", command=self.cancel_auto_start)
        self.countdown_label = tk.Label(root, text="")
        
        self.initialize_with_saved_values()
        
        if self.time_in_seconds > 0 and self.scripts:
            self.edit_button.grid(row=9, column=0, columnspan=2, pady=5)
            self.countdown_label.grid(row=10, column=0, columnspan=2)
            self.start_countdown(10)

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.time_in_seconds = config.get('time_in_seconds', 0)
                self.scripts = config.get('scripts', [])
        except FileNotFoundError:
            pass

    def save_config(self):
        config = {
            'time_in_seconds': self.time_in_seconds,
            'scripts': self.scripts
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f)

    def initialize_with_saved_values(self):
        if self.time_in_seconds > 0:
            hours = self.time_in_seconds // 3600
            minutes = (self.time_in_seconds % 3600) // 60
            seconds = self.time_in_seconds % 60
            self.hours.insert(0, str(hours))
            self.minutes.insert(0, str(minutes))
            self.seconds.insert(0, str(seconds))
        
        for script in self.scripts:
            self.script_list.insert(tk.END, script)

    def start_countdown(self, seconds):
        self.auto_start = True
        def update_countdown(remaining):
            if not self.auto_start or remaining < 0:
                return
            self.countdown_label.config(text=f"Automatischer Start in {remaining} Sekunden...")
            if remaining == 0:
                self.start_scripts()
            else:
                self.root.after(1000, update_countdown, remaining - 1)
        update_countdown(seconds)

    def cancel_auto_start(self):
        self.auto_start = False
        self.edit_button.grid_forget()
        self.countdown_label.grid_forget()

    def save_time(self):
        try:
            hours = int(self.hours.get() or 0)
            minutes = int(self.minutes.get() or 0)
            seconds = int(self.seconds.get() or 0)
            self.time_in_seconds = hours * 3600 + minutes * 60 + seconds
            self.save_config()
        except ValueError:
            print("Fehler: Bitte geben Sie gültige Zahlen ein!")

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if file_path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, file_path)

    def add_script(self):
        script_path = self.path_entry.get()
        if script_path and os.path.exists(script_path) and script_path.endswith('.py'):
            if script_path not in self.scripts:
                self.scripts.append(script_path)
                self.script_list.insert(tk.END, script_path)
                self.path_entry.delete(0, tk.END)
                self.save_config()
        else:
            print("Fehler: Bitte wählen Sie eine gültige Python-Datei!")

    def delete_script(self):
        selected = self.script_list.curselection()
        if selected:
            index = selected[0]
            self.script_list.delete(index)
            self.scripts.pop(index)
            self.save_config()

    def start_script(self, script):
        if platform.system() == "Windows":
            return subprocess.Popen(
                ['python', script],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            return subprocess.Popen(
                ['xterm', '-e', 'python3', script]
            )

    def close_process(self, process):
        try:
            proc = psutil.Process(process.pid)
            proc.terminate()
            time.sleep(2)
            if proc.is_running():
                proc.kill()
                print(f"Prozess {process.pid} wurde erzwungen beendet")
        except psutil.NoSuchProcess:
            print(f"Prozess {process.pid} war bereits beendet")
        except Exception as e:
            print(f"Fehler beim Schließen des Prozesses {process.pid}: {e}")

    def update_restart_timer(self, start_time):
        while self.running:
            remaining = self.time_in_seconds - int(time.time() - start_time)
            if remaining < 0:
                break
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            seconds = remaining % 60
            self.restart_timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            time.sleep(1)
        if self.running:
            self.restart_timer_label.config(text="Neustart...")

    def run_scripts(self):
        while self.running:
            self.processes = []
            for script in self.scripts:
                try:
                    process = self.start_script(script)
                    self.processes.append(process)
                    print(f"Gestartet: {script} mit PID {process.pid}")
                except Exception as e:
                    print(f"Fehler beim Starten von {script}: {e}")
            
            start_time = time.time()
            if self.timer_thread and self.timer_thread.is_alive():
                self.timer_thread.join()
            self.timer_thread = threading.Thread(target=self.update_restart_timer, args=(start_time,))
            self.timer_thread.daemon = True
            self.timer_thread.start()
            
            time.sleep(self.time_in_seconds)
            
            for process in self.processes:
                self.close_process(process)
            self.processes = []

    def start_scripts(self):
        if not self.time_in_seconds:
            print("Fehler: Bitte erst die Zeit einstellen!")
            return
        if not self.scripts:
            print("Fehler: Bitte fügen Sie mindestens ein Script hinzu!")
            return
            
        self.running = True
        self.edit_button.grid_forget()
        self.countdown_label.grid_forget()
        
        thread = threading.Thread(target=self.run_scripts)
        thread.daemon = True
        thread.start()

    def stop_scripts(self):
        self.running = False
        for process in self.processes:
            self.close_process(process)
        self.processes = []
        self.restart_timer_label.config(text="Gestoppt")
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScriptScheduler(root)
    root.mainloop()