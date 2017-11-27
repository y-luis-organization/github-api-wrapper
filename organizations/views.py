import requests
from django.http import JsonResponse

from organizations.utils import get_page_biggest_repo, get_links

ACCEPT_HEADER = 'application/vnd.github.v3+json'

# Try to use an eager strategy because of API rate limits
PER_PAGE = 100


def get_organizations(request):
    """
    Get number of GitHub organizations
    :param request:
    :return:
    """
    body = requests.get('https://api.github.com/search/users?q=type:org', headers={'Accept': ACCEPT_HEADER}).json()

    response = {'total_count': body['total_count']}

    return JsonResponse(response)


def get_repos(request, organization_name):
    """
    Get number of repos and the biggest one (name and size) for a given organization
    :param request:
    :param organization_name:
    :return:
    """
    response = requests.get('https://api.github.com/orgs/{}'.format(organization_name),
                            headers={'Accept': ACCEPT_HEADER})

    body = response.json()
    print(body)
    response = {'public_repos': body['public_repos']}

    organization_id = body['id']

    repos_response = requests.get(
        'https://api.github.com/organizations/{0}/repos?page=1&per_page={1}'.format(organization_id, PER_PAGE),
        headers={'Accept': ACCEPT_HEADER})

    repos = repos_response.json()

    # biggest repo of the page
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
