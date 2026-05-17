import threading
import customtkinter as ctk
from classes import worker, Task
import random
WIN_WIDTH = 1100
WIN_HEIGHT = 700
TITLE = "ThreadsSimulation"
speed = 2000


class VisualisationWindow:
    def __init__(self, root, scheduler):
        self.scheduler = scheduler
        self.root = root
        self.root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+100+100")
        self.root.resizable(True, True)
        self.root.title(TITLE)
        self.root.configure(bg="#333333")
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=0)  # settings
        self.main_frame.grid_rowconfigure(1, weight=0)  # threads
        self.main_frame.grid_rowconfigure(2, weight=1)  # users list

        # settings
        self.settings_frame = ctk.CTkFrame(self.main_frame)
        self.settings_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.start_button = ctk.CTkButton(self.settings_frame, text="Add all",
                                          width=40, height=20, command=self.start_simulation)
        self.start_button.grid(row=0, column=2, pady=10, padx=10)
        self.add_user_button = ctk.CTkButton(self.settings_frame, text="Add user",
                                             width=40, height=20, command=self.add_user)
        self.add_user_button.grid(row=0, column=4)
        
        self.users_entry = ctk.CTkEntry(self.settings_frame, width=60)
        self.users_entry.insert(0, "5")
        self.users_entry.grid(row=2, column=1, padx=5, pady=5)
        self.users_entry_label = ctk.CTkLabel(self.settings_frame, text="Users", text_color="gray")
        self.users_entry_label.grid(row=1, column=1, padx=5, pady=5)

        self.disk_speed_entry = ctk.CTkEntry(self.settings_frame, width=80)
        self.disk_speed_entry.insert(0, "1000")
        self.disk_speed_entry.grid(row=2, column=2, padx=5, pady=5)
        self.disk_speed_label = ctk.CTkLabel(self.settings_frame, text="Disk speed", text_color="gray")
        self.disk_speed_label.grid(row=1, column=2, padx=5, pady=5)

        self.min_size_entry = ctk.CTkEntry(self.settings_frame, width=80)
        self.min_size_entry.insert(0, "1")
        self.min_size_entry.grid(row=2, column=4, padx=5, pady=5)
        self.min_size_label = ctk.CTkLabel(self.settings_frame, text="Min size", text_color="gray")
        self.min_size_label.grid(row=1, column=4, padx=5, pady=5)

        self.max_size_entry = ctk.CTkEntry(self.settings_frame, width=80)
        self.max_size_entry.insert(0, "30000")
        self.max_size_entry.grid(row=2, column=5, padx=5, pady=5)
        self.max_size_label = ctk.CTkLabel(self.settings_frame, text="Max size", text_color="gray")
        self.max_size_label.grid(row=1, column=5, padx=5, pady=5)

        # threads
        self.threads_frame = ctk.CTkFrame(self.main_frame, height=190)
        self.threads_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.threads_frame.pack_propagate(False)
        thread_title = ctk.CTkLabel(self.threads_frame, text="AVAILABLE THREADS",
                                    text_color="#115511", font=("Berlin Sans FB", 24))
        thread_title.pack(side='top', expand=True, pady=(15, 10))
        self.threads_labels = []

        # users
        self.users_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.users_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.users_widgets = {}

        for i in range(5):

            thread = ctk.CTkFrame(self.threads_frame, width=170,  height=100, fg_color="#aaa", corner_radius=10)
            thread.pack(side='left', padx=5, pady=(5, 10), expand=True)
            thread.pack_propagate(False)
            thread_label = ctk.CTkLabel(thread, text=f"Thread {i + 1}", width=80, text_color="#005500", font=("Berlin Sans FB", 20, "bold"))
            thread_label.pack(pady=(20, 10))
            status_label = ctk.CTkLabel(thread, text="Awaiting...", font=("Berlin Sans FB", 15), text_color="gray")
            status_label.pack(padx=20, pady=(2, 10))
            self.threads_labels.append(status_label)

    def start_simulation(self):
        self.start_button.configure(state="disabled")
        users = int(self.users_entry.get())
        min_size = int(self.min_size_entry.get())
        max_size = int(self.max_size_entry.get())
        speed = int(self.disk_speed_entry.get())
        for user_id in range(users):
            for i in range(random.randint(5, 25)):
                file_size = random.randint(min_size, max_size)
                self.scheduler.add_task(Task(user_id, file_size))

        # if not hasattr(self.scheduler, "started"):
        if not len(self.scheduler.threads) == 5:
            self.scheduler.start_threads(5, speed)
            # self.scheduler.started = True
        self.update()

    def add_user(self):
        users_dictionary = self.scheduler.user_tasks_count.copy()
        current_users = set(users_dictionary.keys())
        user_id = max(current_users, default=-1) + 1

        min_size = int(self.min_size_entry.get())
        max_size = int(self.max_size_entry.get())

        # if not hasattr(self.scheduler, "started"):
        if not len(self.scheduler.threads) == 5:
            self.scheduler.start_threads(5, int(self.disk_speed_entry.get()))
            # self.scheduler.started = True

        for i in range(random.randint(5, 25)):
            file_size = random.randint(min_size, max_size)
            self.scheduler.add_task(Task(user_id, file_size))
        self.update()

    def update(self):
        self.disk_speed_entry.configure(state="disabled")
        with self.scheduler.lock:
            active_tasks = self.scheduler.currently_processing[:]
            waiting = sum(len(q) for q in (self.scheduler.user_queues.values()))
            users = len(self.scheduler.user_tasks_count)
            users_dictionary = self.scheduler.user_tasks_count.copy()

            current_users = set(users_dictionary.keys())
            existing_users = set(self.users_widgets.keys())

            for user_id in current_users - existing_users:
                user = ctk.CTkFrame(self.users_frame, width=100, height=60)
                user.grid(row=user_id, column=0, padx=10, pady=10)

                user_label = ctk.CTkLabel(user, text=f"User", font=("Arial", 12, "bold"))
                user_label.pack()
                self.users_widgets[user_id] = (user, user_label)

            for i in range(5):
                if i < len(active_tasks):
                    task = active_tasks[i]
                    self.threads_labels[i].configure(text=f"User: {task.user_id + 1}\nSize: {task.file_size}",
                                                     text_color="green")
                else:
                    self.threads_labels[i].configure(text="Awaiting...", text_color="gray")

            for user_id in current_users:
                _, label = self.users_widgets[user_id]
                label.configure(text=f"User {user_id + 1}\n{users_dictionary[user_id]} files")

            for user_id in existing_users - current_users:
                frame, _ = self.users_widgets[user_id]
                frame.destroy()
                del self.users_widgets[user_id]

            self.root.after(200, self.update)
