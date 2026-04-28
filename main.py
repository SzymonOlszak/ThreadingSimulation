import threading
import time
import math
import random

import customtkinter

from interface import VisualisationWindow
from classes import Scheduler, Task, worker, speed
import customtkinter as CTk


def main():
    scheduler = Scheduler()

    for user_id in range(5):
        for i in range(random.randint(5, 50)):
            file_size = random.randint(1, 500000)
            scheduler.add_task(Task(user_id, file_size))

    root = customtkinter.CTk()
    app = VisualisationWindow(root, scheduler)

    # threads = []
    # for i in range(5):
    #     t = threading.Thread(target=worker, args=(scheduler, speed), daemon=True)
    #     t.start()
    #     threads.append(t)

    root.mainloop()


if __name__ == "__main__":
    main()









# import threading
# import time
# import queue
# import random
# import math
# import itertools
#
# # def thread_func():
# #     print('Thread')
#
# queue = queue.PriorityQueue()
# threads = 5
# speed = 1000  # MB/s
#
# class Task:
#     lock = threading.Lock()
#     count_users = []
#
#     def __init__(self, user_id, file_size):
#         self.user_id = user_id
#         self.file_size = file_size
#         self.created_at = time.time()
#         self.count_users.append(self.user_id)
#
#     @property
#     def priority(self):
#         waiting_time_factor = (math.sqrt(time.time() - self.created_at)) / len(self.count_users)
#         file_size_factor = len(self.count_users) / (1 + math.sqrt(self.file_size))
#         return file_size_factor + waiting_time_factor
#
#     def remove_user(self):
#         print("Removing user", self.user_id)
#
#     def upload(self):
#         with self.lock:
#             self.count_users.remove(self.user_id)
#
#     def __lt__(self, other):
#         return self.priority() < other.priority()
#
#     def __exit__(self):
#         self.remove_user()
#
#
# user1 = Task(1, 870264)
# user2 = Task(2, 1590)
# user3 = Task(3, 30000)
# users = [user1, user2, user3]
# def comparison(el1, el2):
#     if el1.prioryty < el2.prioryty:
#         print("el1 wins")
#     else:
#         print("el2 wins")
#
#
#
# for a, b in itertools.combinations(users, 2):
#     comparison(a, b)
# # def crawl(link, delay=3):
# #     print(f"crawl started for {link}")
# #     time.sleep(delay)  # Blocking I/O (simulating a network request)
# #     print(f"crawl ended for {link}")
# #
# # links = [
# #     "https://python.org",
# #     "https://docs.python.org",
# #     "https://peps.python.org",
# # ]
# #
# # # Start threads for each link
# # threads = []
# # for link in links:
# #     # Using `args` to pass positional arguments and `kwargs` for keyword arguments
# #     t = threading.Thread(target=crawl, args=(link,), kwargs={"delay": 2})
# #     threads.append(t)
# #
# # # Start each thread
# # for t in threads:
# #     t.start()
# #
# # # Wait for all threads to finish
# # for t in threads:
# #     t.join()