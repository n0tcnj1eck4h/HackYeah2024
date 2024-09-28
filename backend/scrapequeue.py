from datetime import time
import datetime
from enum import Enum
from threading import Thread
from typing import List, Optional, Tuple
import time

from flask import Flask
from app import db


class FinishedScrape:
    pass


class ScrapingState(Enum):
    NOTQUEUED = 1
    QUEUED = 2
    SCRAPED = 3


class ScrapeQueue:
    queue: List[str]
    thread: Thread
    should_stop: bool
    app: Flask

    def __init__(self, app: Flask):
        self.queue = []
        self.thread = Thread(target=self.task)
        self.should_stop = True
        self.finished_scrapes = {}
        self.app = app

    def start_thread(self):
        self.should_stop = False
        self.thread.start()

    def stop_thread(self):
        self.should_stop = True
        self.thread.join()

    def task(self):
        while not self.should_stop:
            if len(self.queue) == 0:
                time.sleep(1)
                continue
            url = self.queue.pop()
            self._scrape(url)

    def push(self, url):
        from models import Site

        site = Site.query.filter_by(url=url).first()
        if site is not None:
            return ""

        self.queue.insert(0, url)
        return ""

    def task_status(self, url: str) -> Tuple[ScrapingState, Optional[FinishedScrape]]:
        from models import Site

        if url in self.queue:
            return ScrapingState.QUEUED, None

        site = Site.query.filter_by(url=url).first()
        if site is None:
            return ScrapingState.NOTQUEUED, None

        return ScrapingState.SCRAPED, site

    def _scrape(self, url: str):
        with self.app.app_context():
            from models import Site

            bogus_site = Site()
            bogus_site.url = url
            bogus_site.trust_score = 0
            bogus_site.date_added = datetime.datetime.now()

            db.session.add(bogus_site)
            db.session.commit()
