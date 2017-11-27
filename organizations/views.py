import requests
from django.http import JsonResponse

from organizations.utils import get_page_biggest_repo, get_links

ACCEPT_HEADER = 'application/vnd.github.v3+json'

# Try to use an eager strategy because of API rate limits
PER_PAGE = 100


def get_organizations(request):
    organizations_response = requests.get('https://api.github.com/organizations?per_page={0}'.format(PER_PAGE),
                                          headers={'Accept': ACCEPT_HEADER})

    organizations = organizations_response.json()

    count = len(organizations)

    link_header = organizations_response.headers.get('Link')

    # Follow links
    while link_header is not None:
        links = get_links(link_header)

        if links.get('next') is not None:
            next = requests.get(links.get('next'), headers={'Accept': ACCEPT_HEADER})

            # API rate limit exceeded
            if next.status_code == 403:
                return JsonResponse(next.content, status=403)

            count += len(next.json())

            link_header = next.headers.get('Link')

    response = {'organizations': count}

    return JsonResponse(response)


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

    # Follow links
    if link_header is not None:

        links = get_links(link_header)

        if links.get('next') is not None:
            next = requests.get(links.get('next'), headers={'Accept': ACCEPT_HEADER})

            # API rate limit exceeded
            if next.status_code == 403:
                return JsonResponse(next.content, status=403)

            next_biggest_repo = get_page_biggest_repo(next.json())

            if next_biggest_repo[1] > biggest_repo[1]:
                biggest_repo = next_biggest_repo

    response['biggest_repo'] = {'name': biggest_repo[0], 'size': biggest_repo[1]}

    return JsonResponse(response)
