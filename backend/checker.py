from typing import Optional
import whois
import requests
import urllib.parse
import datetime


class CheckerException(BaseException):
    msg: str

    def __init__(self, msg: str, *args: object) -> None:
        super().__init__(*args)
        self.msg = msg


def legit_check(nip: str, domain: str) -> bool:
    activeVAT = False
    domainRegisterCheck = False
    domainOrgInfoCheck = False
    # czy taka firma istnieje (szukanie po nazwie, nip)

    # czy jest czynnym płatnikiem VAT
    if check_VAT_whitelist(nip) == "Czynny":
        activeVAT = True

    # kiedy zarejestrowano domene (jak nie dawno to źle) rok?
    domainRegisterDate = get_creation_date(domain)
    if domainRegisterDate is not None:
        if type(domainRegisterDate) is list:
            domainRegisterDate = domainRegisterDate[0]

        age = datetime.datetime.now() - domainRegisterDate
        if age > datetime.timedelta(days=365):
            domainRegisterCheck = True

    # czy jest info o org w domenie (jak jest to legit na pewno)
    if get_org_name(domain) is not None:
        domainOrgInfoCheck = True
    if domainOrgInfoCheck:
        return True
    if domainRegisterCheck:
        return True
    if not domainRegisterCheck:
        return False
    if activeVAT:
        return True
    return False


def get_org_name(domain: str) -> Optional[str]:
    domain_info = whois.whois(domain)
    return domain_info.get("org")


def check_VAT_whitelist(nip: str) -> Optional[str]:
    today = datetime.datetime.today()
    today = today.strftime("%Y-%m-%d")
    req = f"https://wl-api.mf.gov.pl/api/search/nip/{nip}?date={today}"
    print(req)
    response = requests.get(req)
    if response.status_code == 200:
        data = response.json()
        try:
            return data["result"]["subject"]["statusVat"]
        except KeyError:
            return None
    else:
        raise CheckerException("bad wl-api request")


def get_creation_date(url: str) -> Optional[datetime.datetime]:
    domain_info = whois.whois(url)
    creation_date = domain_info.get("creation_date")
    if type(creation_date) is list and len(creation_date) > 0:
        return creation_date[0]
    else:
        return creation_date  # this is so ass


def domain_from_whois(urlx: str) -> Optional[str]:
    domain_info = whois.whois(urlx)
    domain_name = domain_info.get("domain_name")
    if domain_name is None:
        return None

    name = None
    if type(domain_name) is list:
        name = domain_name[0]
    elif type(domain_name) is str:
        name = domain_name

    # x jest ignorowane?
    # x = re.match(r"//(.*)", name)
    return name


def krs_to_nip(krs: str) -> str:
    req = f"https://api-krs.ms.gov.pl/api/krs/OdpisAktualny/{krs}?rejestr=P&format=json"
    response = requests.get(req)
    if response.status_code == 200:
        data = response.json()
        try:
            return data["odpis"]["dane"]["dzial1"]["danePodmiotu"]["identyfikatory"][
                "nip"
            ]
        except KeyError:
            raise CheckerException("failed to convert krs to nip")
    else:
        raise CheckerException("bad krs to nip api request")


def name_to_krs(name: str) -> Optional[str]:
    quoted_name = urllib.parse.quote(name)
    req = f"https://dane.biznes.gov.pl/api/mswf/v1/SearchAdvance?companyName={quoted_name}"
    response = requests.get(req)
    if response.status_code == 200:
        data = response.json()
        for company in data["companyList"]:
            krs = company.get("krs")
            if krs is not None:
                return krs
        return None
    elif response.status_code == 204:
        return None
    else:
        raise CheckerException("bad name to krs request")


def nip_to_krs(nip: str) -> dict:
    req = f"https://dane.biznes.gov.pl/api/mswf/v1/SearchAdvance?nip={nip}"
    response = requests.get(req)
    if response.status_code == 200:
        data = response.json()
        try:
            return data["companyList"][0]["krs"]
        except KeyError:
            raise CheckerException("krs not found")
    else:
        raise CheckerException("bad dane.biznes.gov.pl request")
