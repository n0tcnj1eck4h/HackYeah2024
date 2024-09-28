from datetime import time
from threading import Thread
from typing import List, Tuple
import time

class Scrape: 
    pass

class ScrapeQueue:
    queue: List[Tuple[int, str]]
    thread: Thread
    stop: bool
    next_id: int
    finished_scrapes: dict[int, Scrape]

    def __init__(self):
        self.queue = []
        self.thread = Thread(target=self.task)
        self.stop = True
        self.next_id = 0
        self.finished_scrapes = {}

    def start_thread(self):
        self.stop = False
        self.thread.start()

    def stop_thread(self):
        self.stop = True
        self.thread.join()

    def task(self):
        while not self.stop:
            if len(self.queue) == 0:
                time.sleep(1)
                continue
            url = self.queue.pop()
            self._scrape(url[1])

    def push(self, url) -> int:
        id = self.next_id
        self.next_id += 1
        self.queue.insert(0, (id, url))
        return id

    def _scrape(self, url: str):
        pass
