import requests
from django.http import JsonResponse, HttpResponseForbidden

from organizations.utils import get_page_biggest_repo

ACCEPT_HEADER = 'application/vnd.github.v3+json'

# Try to use an eager strategy because of API rate limits
PER_PAGE = 100


def get_organizations(request):
    organizations_response = requests.get('https://api.github.com/organizations?per_page={0}'.format(PER_PAGE),
                                         headers={'Accept': ACCEPT_HEADER})

    organizations = organizations_response.json()

    response = {'organizations': len(organizations)}

    pass


def get_repos(request, organization_name):
    organization_response = requests.get('https://api.github.com/orgs/{}'.format(organization_name),
                                         headers={'Accept': ACCEPT_HEADER})

    organization = organization_response.json()

    response = {'public_repos': organization['public_repos']}

    organization_id = organization['id']

    repos_response = requests.get(
        'https://api.github.com/organizations/{0}/repos?page=1&per_page={1}'.format(organization_id, PER_PAGE),
        headers={'Accept': ACCEPT_HEADER})

    repos = repos_response.json()

    biggest_repo = get_page_biggest_repo(repos)

    link_header = repos_response.headers.get('Link')

    if link_header is not None:

        # Parse Link header as a dictionary
        links = {y[1].split('=')[1].replace('\"', ''): y[0].replace('<', '').replace('>', '') for y in
                 [x.split('; ') for x in link_header.split(', ')]}

        if links.get('next') is not None:
            next = requests.get(links.get('next'), headers={'Accept': ACCEPT_HEADER})

            # API rate limit exceeded
            if next.status_code == 403:
                return HttpResponseForbidden(next.content)

            next_biggest_repo = get_page_biggest_repo(next.json())

            if next_biggest_repo[1] > biggest_repo[1]:
                biggest_repo = next_biggest_repo

    response['biggest_repo'] = {'name': biggest_repo[0], 'size': biggest_repo[1]}

    return JsonResponse(response)
