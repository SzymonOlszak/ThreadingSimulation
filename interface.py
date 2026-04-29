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
        self.start_button = ctk.CTkButton(self.root, text="Add", width=40, height=20, command=self.start_simulation)
        self.start_button.grid(row=0, column=0, columnspan=5, pady=10, padx=10)
        self.threads_labels = []
        self.users_frames = []
        self.users_labels = []

        for i in range(5):
            thread = ctk.CTkFrame(self.root)
            thread.grid(row=1, column = i)
            thread_label = ctk.CTkLabel(thread, text=f"Thread {i + 1}", width=80, font=("Arial", 12, "bold"))
            thread_label.pack(side='top')
            status_label = ctk.CTkLabel(thread, text="Awaiting...", text_color="gray")
            status_label.pack(side="bottom", padx=20)
            self.threads_labels.append(status_label)

        for j in scheduler.user_tasks_count:
            user = ctk.CTkFrame(self.root)
            user.grid(row=2, column=j, padx=10, pady=10)
            user_label = ctk.CTkLabel(user, text=f" User {j + 1}", width=80, font=("Arial", 12, "bold"))
            user_label.pack(side='top')
            user_files_label = ctk.CTkLabel(user, text=f"{scheduler.user_tasks_count[j]} files left", width=80, font=("Arial", 12, "bold"))
            user_label.pack(side='bottom')
            self.users_labels.append(user_label)
            self.users_frames.append(user)

    def start_simulation(self):
        self.start_button.configure(state="disabled")

        for i in range(5):
            t = threading.Thread(target=worker, args=(self.scheduler, speed), daemon=True)
            t.start()

        self.update()

    def update(self):
        with self.scheduler.lock:
            active_tasks = self.scheduler.currently_processing[:]
            waiting = len(self.scheduler.queue)
            users = len(self.scheduler.user_tasks_count)
            users_dictionary = self.scheduler.user_tasks_count.copy()

            for i in range(5):
                if i < len(active_tasks):
                    task = active_tasks[i]
                    self.threads_labels[i].configure(text=f"User: {task.user_id}\nSize: {task.file_size}",
                                                     text_color="green")
                else:
                    self.threads_labels[i].configure(text="Awaiting...", text_color="gray")

            for user_id in range(users):
                count = users_dictionary.get(user_id, 0)
                if count > 0:
                    self.users_labels[user_id].configure(text=f"User {user_id}\n{count} files")
                else:
                    del self.users_frames[user_id]

            self.root.after(200, self.update)
