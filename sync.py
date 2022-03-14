# !/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Manage sync between files and gists for heka-ai-snippet user
"""


# =========================================================================================================
# ================================ 0. MODULE


import os

import click
from api import GithubManager
from api import FilesManager


# =========================================================================================================
# ================================ 1. CREDENTIALS


personal_access_token = os.environ['PERSONAL_ACCESS_TOKEN']


# =========================================================================================================
# ================================ 2. FUNCTION


@click.command()
@click.option('--delete', '-d', is_flag=True, help="whether to delete gists that no longer matches a file")
@click.option('--verbose', '-v', is_flag=True, help="more log printing")
def sync_folder_to_gists(delete, verbose):
    """Synchronizes the content of snippets folder with heka-ai-snippet gists

    Parameters
    ----------
    delete : bool, optional
        Whether to delete gists that no longer matches a file, by default False
    """
    # Connect to wrapper
    heka_ai_snippet = GithubManager('heka-ai-snippets', personal_access_token, verbose=verbose)
    snippet_folder = FilesManager('./snippets')

    # Load both existing gists and files
    gists = heka_ai_snippet.list_gists()
    files = snippet_folder.list_files(get_checksum=True)

    # New files without gists : unicity based on description (saved full path)
    print('Creating new gists', end='...')
    files_to_create_as_gists = [(f, checksum) for (f, checksum) in files if checksum not in [g['description'] for g in gists]]
    if not files_to_create_as_gists:
        print('none')
    else: 
        print('')

    # Create corresponding gists
    for f, checksum in files_to_create_as_gists:
        heka_ai_snippet.create_gists(f, description=checksum, content=snippet_folder.get_file(f))

    # Delete gists that no longer matches a file
    if delete:
        print('Deleting gists without files', end='...')
        if gists_id_without_file := [g['id'] for g in gists if g['description'] not in [checksum for f, checksum in files]]:
            print('')
            heka_ai_snippet.delete_gists(gists_id_without_file)
        else:
            print('none')

    print('Synchronization succedeed!')


# =========================================================================================================
# ================================ 3. EXECUTION


if __name__ == "__main__":
    sync_folder_to_gists()