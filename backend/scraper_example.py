#!/bin/env python3

import checker
from scraper import Scrapper


url = "https://x.com"
scrapper = Scrapper(url)

name = scrapper.get_company_name()
nip = scrapper.get_company_nip()
domain = checker.domain_from_whois(url)

if name is None:
    print("Company name is None... grabbing from domain")
    name = checker.get_org_name(domain)
    print(name)


if nip is None and name is not None:
    krs = checker.name_to_krs(name)
    nip = checker.krs_to_nip(krs)
else:
    print("Both nip and name are None.. damn")
    exit()

if nip is None:
    print("NIP is still None even after krs_to_nip")

check = checker.legit_check(nip, domain)
print(check)
