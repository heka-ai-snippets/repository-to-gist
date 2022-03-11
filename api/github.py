# !/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Classes & functions related to github gists APIs
"""


# =========================================================================================================
# ================================ 0. MODULE


from requests import Session
import json


# =========================================================================================================
# ================================ 1. CLASSES


class GithubManager(object):
    def __init__(self, user, token):
        """Wrapper to manage a few github actions

        Parameters
        ----------
        user : str, optional
            User to connect as
        token : str
            Personal access token with repo-read and gists-create rights
        """
        # Start session
        self.user = user
        self.session = Session()
        self.session.headers['Authorization'] = f'token {token}'
        self.session.headers['Accept'] = 'application/vnd.github.v3+json'

        # Access connection
        con = self.session.get(f'https://api.github.com/users/{self.user}')
        if con.status_code == 200:
            print(f'Connected as {self.user}')
        else:
            print(f'Connection failed\n{con.content}')

    def list_gists(self, user=None, private=False):
        """_summary_

        Parameters
        ----------
        user : str, optional
            User of whom to list gists, by default use current logged in user
        
        private : bool, optional
            List all gists, else only public ones, by default False

        Returns
        -------
        dict
            List of all available gists
        """
        user = self.user if user is None else user
        gists_url = f'https://api.github.com/users/{user}/gists'
        res = []

        for page in [1]:

            get = self.session.get(url=gists_url, 
                                   headers={
                                       'per_page': '100',
                                       'page': f'{page}',
                                       })

            if get.status_code == 200:
                res.extend(get.json())
            else: 
                print(get.content)
                break

        # Extract information
        res = [{
            'id': d['id'],
            'file': d['files'], 
            'description': d['description'],
            'url': d['html_url']} for d in res]

        return res

    def create_gists(self, filename, content, public=True):
        """Create a gist based on some string content

        Parameters
        ----------
        filename : str
            Name of the gist, including the file type
        content : str
            Content of the gists
        public : bool, optional
            Is the gists public or private, by default True

        Returns
        -------
        str
            Id of the newly created gist
        """
        gists_url = 'https://api.github.com/gists'
        data = {
            'public': public,
            'description': filename,
            'files': {
                filename.split('/')[-1]: {
                    'content': content,
                },
            }
        }

        res = self.session.post(gists_url, data=json.dumps(data))

        return res.json()['id']