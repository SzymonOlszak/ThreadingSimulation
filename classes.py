import threading
import time
import math
import random

import tkinter as Tk


class Task:
    def __init__(self, user_id, file_size):
        self.user_id = user_id
        self.file_size = file_size
        self.created_at = time.time()


class Scheduler:
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()
        self.user_tasks_count = {}
        self.currently_processing = []
        self.threads = []
        
    def start_threads(self, threads_count, speed):
        for i in range(threads_count):
            t = threading.Thread(target=worker, args=(self, speed), daemon=True)
            t.start()
            self.threads.append(t)

    def add_task(self, task):
        with self.lock:
            self.queue.append(task)
            if task.user_id not in self.user_tasks_count:
                self.user_tasks_count[task.user_id] = 0

            self.user_tasks_count[task.user_id] += 1
            # self.user_tasks_count[task.user_id] = self.user_tasks_count.get(task.user_id, 0) + 1

    def get_task(self):
        with self.lock:
            if not self.queue:
                return None

            active_users_count = max(1, len(self.user_tasks_count))
            best = max(self.queue, key=lambda t: self.compute_priority(t, active_users_count))

            self.queue.remove(best)
            self.currently_processing.append(best)
            return best

    def complete_task(self, task):
        with self.lock:
            self.user_tasks_count[task.user_id] -= 1
            self.currently_processing.remove(task)

            if self.user_tasks_count[task.user_id] == 0:
                del self.user_tasks_count[task.user_id]
            # if len(self.queue) == 0:
            #     del self.user_tasks_count[task.user_id]

    def compute_priority(self, task, active_users):
        waiting_factor = (time.time() - task.created_at) ** 0.8 / active_users
        size_factor = active_users / (1 + math.sqrt(task.file_size))

        return waiting_factor + size_factor


def worker(scheduler, upload_speed):
    while True:
        task = scheduler.get_task()
        if not task:
            time.sleep(0.1)
            continue

        print(f"Uploading user {task.user_id}, size {task.file_size}")

        time.sleep(task.file_size / upload_speed) # + random.uniform(0.1, 0.5))

        scheduler.complete_task(task)
        print(f"Done user {task.user_id}")






