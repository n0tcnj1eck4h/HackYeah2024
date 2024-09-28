import requests
import re
from LegitChecker import LegitChecker
from Scraper import Scrapper


url = 'https://x.com'
scrapper = Scrapper(url)
legit = LegitChecker()
name = scrapper.get_company_name()
print(name)
nip = scrapper.get_company_nip()
print(nip)
if nip != None:
    legit.nip = nip
if name != None:
    legit.name = name
if name == None and nip == None:
    legit.name_from_whois(url)

print(legit.legit_check())



