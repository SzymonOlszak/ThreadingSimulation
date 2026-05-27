import threading
import customtkinter as ctk
from classes import worker, Task
import random
WIN_WIDTH = 1100
WIN_HEIGHT = 900
TITLE = "ThreadsSimulation"
speed = 2000


class VisualisationWindow:
    def __init__(self, root, scheduler):
        self.scheduler = scheduler
        self.root = root
        self.root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}+100+100")
        self.root.resizable(True, True)
        self.root.title(TITLE)
        self.root.configure(bg="#888888")
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#717171")
        self.main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=0)  # settings
        self.main_frame.grid_rowconfigure(1, weight=0)  # threads
        self.main_frame.grid_rowconfigure(2, weight=1)  # users list

        # settings
        self.settings_frame = ctk.CTkFrame(self.main_frame, fg_color="#323232")
        self.settings_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        for i in range(5):
            self.settings_frame.grid_columnconfigure(i, weight=1)

        button_font = ("Berlin Sans FB", 22, "bold")
        label_font = ("Berlin Sans FB", 20)
        entry_font = ("Berlin Sans FB", 18)

        # ----BUTTONS
        # self.buttons_frame = ctk.CTkFrame(self.settings_frame)
        # self.buttons_frame.grid(row=2, column=1, columnspan=3, sticky="ew", padx=10, pady=10)
        #
        # self.start_button = ctk.CTkButton(
        #     self.buttons_frame,
        #     text="Add all",
        #     width=180,
        #     height=45,
        #     font=button_font,
        #     fg_color="#55aa00",
        #     hover_color="#99ff99",
        #     text_color="#000000",
        #     command=self.start_simulation
        # )
        # self.start_button.pack(side='left', padx=(150,0))

        self.add_user_button = ctk.CTkButton(
            self.settings_frame,
            text="Add users",
            width=180,
            height=45,
            font=button_font,
            fg_color="#55aa00",
            hover_color="#449900",
            text_color="#113311",
            command=self.add_user
        )
        self.add_user_button.grid(row=2, column=2, pady=10)

        # ------ENTRIES
        self.users_entry = ctk.CTkEntry(
            self.settings_frame,
            width=120,
            height=40,
            justify="center",
            fg_color="#dddddd",
            font=entry_font
        )
        self.users_entry.insert(0, "5")
        self.users_entry.grid(row=1, column=2, pady=(0, 10))

        self.users_entry_label = ctk.CTkLabel(
            self.settings_frame,
            text="Users",
            font=label_font,
            text_color="#55aa00"
        )
        self.users_entry_label.grid(row=0, column=2, padx=50, pady=(10, 0))


        # self.disk_speed_entry = ctk.CTkEntry(self.settings_frame, width=80)
        # self.disk_speed_entry.insert(0, "1000")
        # self.disk_speed_entry.grid(row=2, column=2, padx=5, pady=5)
        # self.disk_speed_label = ctk.CTkLabel(self.settings_frame, text="Disk speed", text_color="gray")
        # self.disk_speed_label.grid(row=1, column=2, padx=5, pady=5)

        self.min_size_entry = ctk.CTkEntry(
            self.settings_frame,
            width=120,
            height=40,
            justify="center",
            fg_color="#dddddd",
            font=entry_font
        )
        self.min_size_entry.insert(0, "1")
        self.min_size_entry.grid(row=1, column=0, padx=(50, 0), pady=(0, 10))
        self.min_size_label = ctk.CTkLabel(
            self.settings_frame,
            text="Min size",
            font=label_font,
            text_color="#55aa00"
        )
        self.min_size_label.grid(row=0, column=0, padx=(50, 0), pady=(10, 0))

        self.max_size_entry = ctk.CTkEntry(
            self.settings_frame,
            width=120,
            height=40,
            justify="center",
            fg_color="#dddddd",
            font=entry_font
        )
        self.max_size_entry.insert(0, "30000")
        self.max_size_entry.grid(row=1, column=1, pady=(0, 10), sticky='w')

        self.max_size_label = ctk.CTkLabel(
            self.settings_frame,
            text="Max size",
            font=label_font,
            text_color="#55aa00"
        )
        self.max_size_label.grid(row=0, column=1, padx=(25, 0), pady=(10, 0), sticky='w')

        self.min_files_entry = ctk.CTkEntry(
            self.settings_frame,
            width=120,
            height=40,
            justify="center",
            fg_color="#dddddd",
            font=entry_font
        )
        self.min_files_entry.insert(0, "1")
        self.min_files_entry.grid(row=1, column=3, pady=(0, 10), sticky='e')

        self.min_files_label = ctk.CTkLabel(
            self.settings_frame,
            text="Min files",
            font=label_font,
            text_color="#55aa00"
        )
        self.min_files_label.grid(row=0, column=3, padx=(0, 28), pady=(10, 5), sticky='e')

        self.max_files_entry = ctk.CTkEntry(
            self.settings_frame,
            width=120,
            height=40,
            justify="center",
            fg_color="#dddddd",
            font=entry_font
        )
        self.max_files_entry.insert(0, "25")
        self.max_files_entry.grid(row=1, column=4, padx=(0,50), pady=(0, 10))

        self.max_files_label = ctk.CTkLabel(
            self.settings_frame,
            text="Max files",
            font=label_font,
            text_color="#55aa00"
        )
        self.max_files_label.grid(row=0, column=4, padx=(0, 50), pady=(10, 5))

        # threads
        self.threads_frame = ctk.CTkFrame(self.main_frame, height=190, fg_color="#323232")
        self.threads_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.threads_frame.pack_propagate(False)
        thread_title = ctk.CTkLabel(self.threads_frame, text="AVAILABLE THREADS",
                                    text_color="#65ba00", font=("Berlin Sans FB", 24))
        thread_title.pack(side='top', expand=True, pady=(15, 10))
        self.threads_labels = []

        # users
        self.users_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="#777777")
        self.users_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        for i in range(3):
            self.users_frame.grid_columnconfigure(i, weight=1)
        self.users_widgets = {}

        for i in range(5):

            thread = ctk.CTkFrame(self.threads_frame, width=170,  height=100, fg_color="#aaa", corner_radius=10)
            thread.pack(side='left', padx=5, pady=(5, 10), expand=True)
            thread.pack_propagate(False)
            thread_label = ctk.CTkLabel(thread, text=f"Thread {i + 1}", width=80, text_color="#126500", font=("Berlin Sans FB", 20, "bold"))
            thread_label.pack(pady=(20, 10))
            status_label = ctk.CTkLabel(thread, text="Awaiting...", font=("Berlin Sans FB", 15), text_color="gray")
            status_label.pack(padx=20, pady=(2, 10))
            self.threads_labels.append(status_label)

        self.update()

    def add_user(self):
        users = int(self.users_entry.get())
        for _ in range(users):
            users_dictionary = self.scheduler.user_tasks_count.copy()
            current_users = set(users_dictionary.keys())
            user_id = 0
            while user_id in current_users:          # First free ID
                user_id += 1
            # user_id = max(current_users, default=-1) + 1

            min_size = int(self.min_size_entry.get())
            max_size = int(self.max_size_entry.get())
            min_files = int(self.min_files_entry.get())
            max_files = int(self.max_files_entry.get())
            # if not hasattr(self.scheduler, "started"):
            if not len(self.scheduler.threads) == 5:
                self.scheduler.start_threads(5, 5000)
                # self.scheduler.started = True

            tasks_count = random.randint(min_files, max_files)

            self.scheduler.initial_user_tasks[user_id] = tasks_count

            for _ in range(tasks_count):
                file_size = random.randint(min_size, max_size)
                self.scheduler.add_task(Task(user_id, file_size))

    def update(self):
        # self.disk_speed_entry.configure(state="disabled")
        with self.scheduler.lock:
            active_tasks = self.scheduler.currently_processing[:]
            waiting = sum(len(q) for q in (self.scheduler.user_queues.values()))
            users = len(self.scheduler.user_tasks_count)
            users_dictionary = self.scheduler.user_tasks_count.copy()

            current_users = set(users_dictionary.keys())
            existing_users = set(self.users_widgets.keys())

            for user_id in current_users - existing_users:
                user = ctk.CTkFrame(
                    self.users_frame,
                    corner_radius=15,
                    fg_color="#2f2f2f"
                )
                user.grid(row=user_id, column=0, padx=15, pady=8, sticky="ew")

                user.grid_propagate(False)

                # LEFT SIDE
                left_frame = ctk.CTkFrame(user, fg_color="transparent")
                left_frame.pack(side="left", padx=20, pady=10, anchor="w")

                user_label = ctk.CTkLabel(
                    left_frame,
                    text=f"USER {user_id + 1}",
                    font=("Berlin Sans FB", 22, "bold"),
                    text_color="#55aa00"
                )
                user_label.pack(padx=(30, 0))

                files_label = ctk.CTkLabel(
                    left_frame,
                    text="0 files left",
                    font=("Berlin Sans FB", 16),
                    text_color="lightgray",
                )
                files_label.pack(padx=(30, 0))

                # RIGHT SIDE
                right_frame = ctk.CTkFrame(user, fg_color="transparent")
                right_frame.pack(side="right", padx=20)

                next_file_label = ctk.CTkLabel(
                    right_frame,
                    text="Next: ---",
                    font=("Berlin Sans FB", 16),
                    text_color="#cccccc"
                )
                next_file_label.pack(pady=(12, 5))

                progress = ctk.CTkProgressBar(
                    right_frame,
                    width=300,
                    height=18
                )
                progress.set(0)
                progress.pack()

                self.users_widgets[user_id] = {
                    "frame": user,
                    "user_label": user_label,
                    "files_label": files_label,
                    "next_file_label": next_file_label,
                    "progress": progress
                }

            for i in range(5):
                if i < len(active_tasks):
                    task = active_tasks[i]
                    self.threads_labels[i].configure(text=f"User: {task.user_id + 1}\nSize: {task.file_size}",
                                                     text_color="green")
                else:
                    self.threads_labels[i].configure(text="Awaiting...", text_color="gray")

            for user_id in current_users:
                # _, label = self.users_widgets[user_id]
                # label.configure(text=f"User {user_id + 1}\n{users_dictionary[user_id]} files")
                widgets = self.users_widgets[user_id]

                widgets["files_label"].configure(
                    text=f"{users_dictionary[user_id]} files left"
                )

                queue = self.scheduler.user_queues.get(user_id, [])

                if queue:
                    _, _, _, next_task = queue[0]

                    widgets["next_file_label"].configure(
                        text=f"Next file: {next_task.file_size} MB"
                    )
                else:
                    widgets["next_file_label"].configure(
                        text="Queue empty"
                    )

                initial_files = self.scheduler.initial_user_tasks.get(user_id, 1)
                progress_value = 1 - (users_dictionary[user_id] / initial_files)

                widgets["progress"].set(progress_value)

            for user_id in existing_users - current_users:
                widgets = self.users_widgets[user_id]
                widgets["frame"].destroy()
                del self.users_widgets[user_id]

            self.root.after(200, self.update)
