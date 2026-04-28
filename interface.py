import threading
import customtkinter as ctk
from classes import worker, speed
WIN_WIDTH = 600
WIN_HEIGHT = 300
TITLE = "ThreadsSimulation"


class VisualisationWindow:
    def __init__(self, root, scheduler):
        self.scheduler = scheduler
        self.root = root
        self.root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+100+100")
        self.root.resizable(False, False)
        self.root.title(TITLE)
        self.root.configure(bg = "#333333")
        self.update()
        self.start_button = ctk.CTkButton(self.root, text="Add", width=40, height=20, command=self.start_simulation)
        self.start_button.grid(row=0, column=0, columnspan=5, pady=10, padx=10)
        self.threads_labels = []

        for i in range(5):
            thread = ctk.CTkFrame(self.root)
            thread.grid(row=1, column = i)
            thread_label = ctk.CTkLabel(thread, text=f"Thread {i + 1}", width=80, font=("Arial", 12, "bold"))
            thread_label.pack(side='top')
            status_label = ctk.CTkLabel(thread, text="Awaiting...", text_color="gray")
            status_label.pack(side="bottom", padx=20)
            self.threads_labels.append(status_label)

    def start_simulation(self):
        self.start_button.configure(state="disabled")

        for i in range(5):
            t = threading.Thread(target=worker, args=(self.scheduler, speed), daemon=True)
            t.start()

    def update(self):
        with self.scheduler.lock:
            active_tasks = self.scheduler.currently_processing[:]
            waiting = len(self.scheduler.queue)
            users = len(self.scheduler.user_tasks_count)

            for i in range(5):
                self.threads_labels[i].configure()