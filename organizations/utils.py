def get_page_biggest_repo(repos):
    """
    Get biggest repo
    :param repos: List of JSON repos
    :return: Tuple with repo name and repo size
    """
    biggest_repo = ('', 0)

    for repo in repos:
        if repo['size'] > biggest_repo[1]:
            biggest_repo = (repo['name'], repo['size'])

    return biggest_repo


def get_links(link_header):
    """
    Parse Link header
    :return: Links as a dictionary
    """
    return {y[1].split('=')[1].replace('\"', ''): y[0].replace('<', '').replace('>', '') for y in
             [x.split('; ') for x in link_header.split(', ')]}