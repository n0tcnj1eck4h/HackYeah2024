from typing import Optional
import requests
import re
from bs4 import BeautifulSoup


class Scrapper:
    # page_url = 'https://www.morele.net'
    url = ""

    # dupa = BeautifulSoup(page.content, 'html.parser')
    # dupa = dupa.footer
    # print(dupa.encode("utf-8"))

    # szukanie nip
    pattern = r"\b\d{3}[-]?\d{2}[-]?\d{2}[-]?\d{3}\b"
    # szukanie nazwy firmy
    pattern2 = r"\b[\w\s.,&'-]+ (sp. z o.o.|s.a.)\b"
    # szukanie mail
    pattern3 = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}"

    # companyNip  = re.search(pattern,  str(dupa))
    # companyName = re.search(pattern2, str(dupa))
    # companyMail = re.search(pattern3, str(dupa))

    # print(str(dupa.encode("utf-8")))
    # print(companyNip)
    # print(companyName)
    # print(companyMail)

    def __init__(self, url):
        self.url = url

    def get_webpage_footer(self):
        page = requests.get(self.url)
        bsPage = BeautifulSoup(page.content, "html.parser")
        bsPage = bsPage.footer

        return bsPage

    def get_company_nip(self) -> Optional[str]:
        footer = self.get_webpage_footer()
        companyNip = re.search(self.pattern, str(footer))

        return companyNip

    def get_company_name(self) -> Optional[str]:
        footer = self.get_webpage_footer()
        companyName = re.search(self.pattern2, str(footer))

        return companyName

    def get_company_mail(self) -> Optional[str]:
        footer = self.get_webpage_footer()
        companyMail = re.search(self.pattern3, str(footer))

        return companyMail
