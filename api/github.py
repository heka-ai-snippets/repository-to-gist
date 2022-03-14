# !/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Classes & functions related to github gists APIs

ref:
    * https://docs.github.com/en/rest/reference/gists
"""


# =========================================================================================================
# ================================ 0. MODULE


from requests import Session
import json


# =========================================================================================================
# ================================ 1. CLASSES


class GithubManager(object):
    def __init__(self, user, token, verbose=True):
        """Wrapper to manage a few github actions

        Parameters
        ----------
        user : str, optional
            User to connect as
        token : str
            Personal access token with repo-read and gists-create rights
        """
        self.verbose = verbose

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
        print(f'Listing gists for {user}...')

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
                break

        # Extract information
        res = [{
            'id': d['id'],
            'gist_name': list(d['files'].keys())[0], 
            'description': d['description'],
            'url': d['html_url']} for d in res]

        return res

    def create_gists(self, filename, description, content, public=True):
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
            'description': description,
            'files': {
                filename.split('/')[-1]: {
                    'content': content,
                },
            }
        }

        res = self.session.post(gists_url, data=json.dumps(data))

        if self.verbose:
            if (res.status_code // 100) == 2:
                print(f'    {filename}: created!')
            else:
                print(f'    {filename}: failed ({res.json()["message"]})')

        return res.json()['id']

    def delete_gists(self, gists_id):
        """Delete github gists

        Parameters
        ----------
        gists_id : List[str]
            List of gist ids to delete 
        """
        gists_url = 'https://api.github.com/gists/'
        for id in gists_id:
            res = self.session.delete(gists_url + id)

            if self.verbose:
                if (res.status_code // 100) == 2:
                    print(f'    {id}: deleted!')
                else:
                    print(f'    {id}: {res.json()["message"]}')