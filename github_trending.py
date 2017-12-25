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
    url = 'https://api.github.com/search/repositories'
    trending_repos = requests.get(
        url,
        params=search_params
    ).json()['items']
    return trending_repos


def get_open_issues(repositories):
    issues = []
    for repository in repositories:
        url = 'https://api.github.com/repos/{}/issues'.format(
            repository['full_name']
        )
        issues.append(requests.get(url).json())
    return issues


def print_repositories_info(repositories, issues):
    for repo, issue in zip(repositories, issues):
        print('Repo Owner: \t\t{}'.format(repo['owner']['login']))
        print('Repo Name: \t\t{}'.format(repo['name']))
        print('Open Issues Amount: \t{}'.format(len(issue)))
        print('Repo Link: \t\t{}'.format(repo['html_url']))
        print('-' * 80)


if __name__ == '__main__':
    trending_repos_quantity = 20
    trending_repositories = get_trending_repositories(trending_repos_quantity)
    open_issues = get_open_issues(trending_repositories)
    print_repositories_info(trending_repositories, open_issues)
