import threading
import time
import math
import random
import heapq
from collections import deque
import tkinter as Tk
from collections import defaultdict


class Task:
    def __init__(self, user_id, file_size):
        self.user_id = user_id
        self.file_size = file_size
        self.created_at = time.time()


class Scheduler:
    def __init__(self):
        self.lock = threading.Lock()
        self.user_tasks_count = defaultdict(int)
        self.currently_processing = []
        self.threads = []
        self.user_queues = {}

    def start_threads(self, threads_count, speed):
        for i in range(threads_count):
            t = threading.Thread(target=worker, args=(self, speed), daemon=True)
            t.start()
            self.threads.append(t)

    def add_task(self, task):
        with self.lock:
            if task.user_id not in self.user_queues:
                self.user_queues[task.user_id] = []

            heapq.heappush(
                self.user_queues[task.user_id],
                (task.file_size, task.created_at, task)
            )

            self.user_tasks_count[task.user_id] += 1

    def get_task(self):
        with self.lock:
            if not self.user_queues:
                return None
            active_users_count = len(self.user_queues)
            candidates = []

            for user_id, queue in self.user_queues.items():

                if queue:
                    _, _, task = queue[0]

                    priority = self.compute_priority(task,  max(1, active_users_count))
                    candidates.append((priority, user_id, task))

            if not candidates:
                return None

            _, best_user_id, best_task = max(candidates, key=lambda x: x[0])

            heapq.heappop(self.user_queues[best_user_id])

            # active_users_count = max(1, len(self.user_tasks_count))
            # best = max(self.queue, key=lambda t: self.compute_priority(t, active_users_count))
            #
            # self.queue.remove(best)
            self.currently_processing.append(best_task)
            return best_task

    def complete_task(self, task):
        with self.lock:
            self.user_tasks_count[task.user_id] -= 1
            self.currently_processing.remove(task)

            if self.user_tasks_count[task.user_id] == 0:
                del self.user_tasks_count[task.user_id]
            if not self.user_queues[task.user_id]:
                del self.user_queues[task.user_id]

    @staticmethod
    def compute_priority(task, active_users):
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






