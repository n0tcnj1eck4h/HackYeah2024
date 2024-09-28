import whois
import requests
import urllib.parse
import datetime
import re

class LegitChecker:
    nip:str=''
    krs:str=''
    name:str=''
    url:str=''

    def __init__(self, name='' ,nip='', krs='', url=''):
        self.name=name
        self.nip=nip
        self.krs=krs
        self.url=url


    def name_from_whois(self, urlx:str):
        domain_info = whois.whois(urlx)
        if domain_info['domain_name'] == None:
            return ('bad request')
        elif 'domain_name' in domain_info.keys():

            if type(domain_info['domain_name']) is list:
                name = (domain_info['domain_name'][0])
            elif type(domain_info['domain_name']) is str:
                name = domain_info['domain_name']
            x = re.match(r"//(.*)", name)

            self.name = name
            self.url = urlx
            return self.name
        else:
            return ('domain_name')

    # bieze nazwe i zamienia na nip
    def name_to_krs(self) -> str:
        name = urllib.parse.quote(self.name)
        req = f"https://dane.biznes.gov.pl/api/mswf/v1/SearchAdvance?companyName={name}"
        response = requests.get(req)
        if response.status_code == 200:
            data = response.json()
            try:
                return data['companyList'][0]['krs']
            except KeyError as e:
                try:
                    return data['companyList'][1]['krs']
                except KeyError as e:
                    return 'krs not found'
        else:
            return response.status_code()

    def nip_to_krs(self) -> dict:
        req = f"https://dane.biznes.gov.pl/api/mswf/v1/SearchAdvance?nip={self.nip}"
        response = requests.get(req)
        if response.status_code == 200:
            data = response.json()
            try:
                return data['companyList'][0]['krs']
            except KeyError as e:
                return {'error': 'krs not found'}
        else:
            return {"error": response.status_code}

    def krs_to_nip(self):
        req = f"https://api-krs.ms.gov.pl/api/krs/OdpisAktualny/{self.krs}?rejestr=P&format=json"
        response = requests.get(req)
        if response.status_code == 200:
            data = response.json()
            try:
                return data['odpis']['dane']['dzial1']['danePodmiotu']['identyfikatory']['nip']
            except KeyError as e:
                return 'nip not found'
        else:
            return {"error": response.status_code}

    def check_VAT_whitelist(self):
        today = datetime.datetime.today()
        today = today.strftime('%Y-%m-%d')
        req = f"https://wl-api.mf.gov.pl/api/search/nip/{self.nip}?date={today}"
        response = requests.get(req)
        if response.status_code == 200:
            data = response.json()
            try:
                return data['result']['subject']['statusVat']
            except KeyError as e:
                return 'StatusVat not found'
        else:
            return ({"error": response.status_code})

    def get_org_name(self):
        domain_info = whois.whois(self.url)
        if domain_info['domain_name'] == None:
            return ('bad request')
        elif 'org' in domain_info.keys():
            if domain_info['org'] != None:
                return (domain_info['org'])
            else:
                return ('org is None')
        else:
            return ('org not found')

    def get_creation_date(self):
        domain_info = whois.whois(self.url)
        if domain_info['domain_name'] == None:
            return ('bad request')
        elif 'creation_date' in domain_info.keys():
            if domain_info['creation_date'] != None:
                return (domain_info['creation_date'])
            else:
                return ('creation_date is None')
        else:
            return ('creation_date not found')

    def legit_check(self):
        activeVAT = False
        domainRegisterCheck = False
        domainOrgInfoCheck = False
        # czy taka firma istnieje (szukanie po nazwie, nip)

        # czy jest czynnym płatnikiem VAT
        nip = self.krs_to_nip()
        if self.check_VAT_whitelist() == 'Czynny':
            activeVAT = True

        # kiedy zarejestrowano domene (jak nie dawno to źle) rok?
        domainRegisterDate = self.get_creation_date()
        if domainRegisterDate not in ['creation_date is None', 'creation_date not found', 'bad request']:
            if type(domainRegisterDate) is list:
                domainRegisterDate=domainRegisterDate[0]

            age = datetime.datetime.now() - domainRegisterDate
            if age > datetime.timedelta(days=365):
                domainRegisterCheck = True

        # czy jest info o org w domenie (jak jest to legit na pewno)
        if self.get_org_name() not in ['org is None', 'org not found', 'bad request']:
            domainOrgInfoCheck = True
        if domainOrgInfoCheck:
            return True
        if domainRegisterCheck:
            return True
        if not domainRegisterCheck:
            return False
        if activeVAT:
            return True

