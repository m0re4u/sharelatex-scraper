import bs4
import re
import json
import requests
import logging

SHARELATEX_ROOT = "https://www.sharelatex.com"
LOGIN_ADDR = "/login"

logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class LoginManager():
    def __init__(self, credentials):
        """
        Save the credentials for the user we want to download the projects from
        """
        self.credentials = credentials

    def login(self, session):
        """
        Login using the credentials provided by the user
        """
        out = session.get(SHARELATEX_ROOT + LOGIN_ADDR)  # also sets cookie
        csrftoken = self.ask_csrf(out.content)
        logger.debug("CSRF token: {}".format(csrftoken))

        payload = {
            'email': self.credentials['email'],
            'password': self.credentials['password'],
            '_csrf':csrftoken
        }
        login_result = session.post(SHARELATEX_ROOT + LOGIN_ADDR, data=payload)
        # TODO: handle faulty logins

        redr_content = json.loads(login_result.content.decode())
        return SHARELATEX_ROOT + redr_content['redir']

    def ask_csrf(self, html_output):
        """
        Look for the CSRF value in the html on the login page
        """
        soup = bs4.BeautifulSoup(html_output, 'html.parser')
        csrf = [tag['value'] for tag in soup.find_all('input', {'name':'_csrf'})]
        if len(csrf) > 1:
            logger.warn("Multiple csrf tokens found, using first of {}".format(len(csrf)))
        return csrf[0]
