import os
import bs4
import json
import logging
import requests
import zipfile
from io import BytesIO

import login

logger = logging.getLogger(__name__)


class ShareLatexSession():
    def __init__(self, userdata):
        """
        Start a session to ShareLatex
        """
        self.session = requests.Session()
        loginmgr = login.LoginManager(userdata)
        self.project_url = loginmgr.login(self.session)
        logger.debug("Login successful to \'{}\'".format(self.project_url))

    def get_project_list(self):
        """
        Get a list of ShareLatex projects as tuples containing (name, id)
        """
        soup = self.get_parsed_html(self.project_url)
        proj_data = soup.find_all('script', {'id':'data'})
        if len(proj_data) > 1:
            logger.warn("Multiple project data found, using first of {}".format(len(proj_data)))
        proj_json = json.loads(proj_data[0].decode_contents())
        return [(proj['name'], proj['id']) for proj in proj_json['projects']]

    def download_project(self, name, id, out_path):
        """
        Download project id as zip  and extract it to the path given by name
        """
        url = self.project_url + '/' + id + '/download/zip'
        out = self.session.get(url)
        logger.debug("Downloading \'{}\' from {}".format(name, url))
        file = zipfile.ZipFile(BytesIO(out.content))
        file.extractall(os.path.join(out_path, name))

    def get_parsed_html(self, url):
        """
        Parse html from url with BeautifulSoup
        """
        out = self.session.get(url)
        if out.status_code == 404:
            logger.error("Got 404 on {}".format(url))
        return bs4.BeautifulSoup(out.content, 'html.parser')
