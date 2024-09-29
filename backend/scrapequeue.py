from datetime import time
import datetime
from enum import Enum
from threading import Thread
from typing import List, Optional, Tuple
import time
import checker
from models import Site
from flask import Flask
from app import db


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

    def push(self, domain: str):
        site = Site.query.filter_by(domain=domain).first()
        if site is not None:
            return

        self.queue.insert(0, domain)

    def task_status(self, domain: str) -> Tuple[ScrapingState, Optional[Site]]:
        if domain in self.queue:
            return ScrapingState.QUEUED, None

        site = Site.query.filter_by(domain=domain).first()
        if site is None:
            return ScrapingState.NOTQUEUED, None

        return ScrapingState.SCRAPED, site

    def _scrape(self, domain: str):
        with self.app.app_context():
            site = Site()

            # I sure hope nothing fucking crashes or the entire thread goes to shit

            site.domain = domain
            site.org_name = checker.get_org_name(site.domain)  # or scrape

            if site.org_name is not None:
                site.krs = checker.name_to_krs(site.org_name)

            if site.krs is not None:
                site.nip = checker.krs_to_nip(site.krs)

            if site.nip is not None:
                site.active_vat = checker.check_VAT_whitelist(site.nip) == "Czynny"

            site.domain_registration = checker.get_creation_date(domain)

            site.date_added = datetime.datetime.now()

            db.session.add(site)
            db.session.commit()
