def get_page_biggest_repo(repos):
    biggest_repo = ('', 0)

    for repo in repos:
        if repo['size'] > biggest_repo[1]:
            biggest_repo = (repo['name'], repo['size'])

    return biggest_repo