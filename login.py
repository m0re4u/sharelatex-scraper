import bs4
import re
import json
import requests
import logging


SHARELATEX_ROOT = "https://www.sharelatex.com"
LOGIN_ADDR = "/login"
logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)

class LoginSession():
    def __init__(self, credentials):
        self.credentials = credentials
        self.logger = logging.getLogger(__name__)
        self.session = None

    def login(self):
        self.session = requests.Session()
        out = self.session.get(SHARELATEX_ROOT + LOGIN_ADDR)  # also sets cookie
        csrftoken = self.ask_csrf(out.content)
        self.logger.debug(csrftoken)

        payload = {
            'email': self.credentials['email'],
            'password': self.credentials['password'],
            '_csrf':csrftoken
        }
        login_result = self.session.post(SHARELATEX_ROOT + LOGIN_ADDR, data=payload)
        # TODO: handle faulty logins

        redr_content = json.loads(login_result.content.decode())
        self.project_url = SHARELATEX_ROOT + redr_content['redir']

    def ask_csrf(self, html_output):
        soup = bs4.BeautifulSoup(html_output, 'html.parser')
        csrf = [tag['value'] for tag in soup.find_all('input', {'name':'_csrf'})]
        if len(csrf) > 1:
            self.logger.warn("Multiple csrf tokens found, using first of {}".format(len(csrf)))
        return csrf[0]

    def get_project_list(self):
        out = self.session.get(self.project_url)
        soup = bs4.BeautifulSoup(out.content, 'html.parser')
        proj_data = soup.find_all('script', {'id':'data'})
        if len(proj_data) > 1:
            self.logger.warn("Multiple project data found, using first of {}".format(len(proj_data)))
        proj_json = json.loads(proj_data[0].decode_contents())
        return [proj['name'] for proj in proj_json['projects']]

def main():
    pass


if __name__ == '__main__':
    main()
