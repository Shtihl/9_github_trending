#!/usr/bin/env python3

from datetime import datetime
from datetime import timedelta
import requests


def get_trending_repositories(quantity):
    last_week = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    search_params = {
        'q': 'created:>={}'.format(last_week),
        'sort': 'stars',
        'order': 'desc'
    }
    trending_repos = requests.get(
        'https://api.github.com/search/repositories',
        params=search_params
    ).json()['items'][:quantity]
    return trending_repos


def get_repositories_info(repositories):
    repo_info = []
    for repo in repositories:
        repo_owner = repo['owner']['login']
        repo_name = repo['name']
        repo_html_url = repo['html_url']
        issues_quantity = len(
            requests.get(
                'https://api.github.com/repos/{}/{}/issues'.format(
                    repo_owner,
                    repo_name
                )).json())
        repo_info.append({
            'repo_name': repo_name,
            'repo_owner': repo_owner,
            'repo_issues_quantity': issues_quantity,
            'repo_html_url': repo_html_url
        })
    return repo_info


def print_repositories_info(repositories):
    for repo in repositories:
        print('Repo Name: \t\t{}'.format(repo['repo_name']))
        print('Repo Owner: \t\t{}'.format(repo['repo_owner']))
        print('Open Issues Amount: \t{}'.format(repo['repo_issues_quantity']))
        print('Repo Link: \t\t{}'.format(repo['repo_html_url']))
        print('-' * 80)


if __name__ == '__main__':
    trending_repos_quantity = 20
    trending_repositories = get_trending_repositories(trending_repos_quantity)
    trending_repositories_info = get_repositories_info(trending_repositories)
    print_repositories_info(trending_repositories_info)
