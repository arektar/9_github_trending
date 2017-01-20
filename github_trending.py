import requests
import datetime
import json


def take_least_days_github_posts(days_before_look=7):
    delta = datetime.timedelta(days=days_before_look)
    now_date = datetime.date.today()
    take_from_date = now_date - delta
    request = "https://api.github.com/search/repositories"
    my_params = {'q': 'pushed:>=%s' % (take_from_date), 'sort': 'stars', 'order': 'desc'}
    response = requests.get(request, params=my_params)
    return response.text


def get_trending_repositories(top_size):
    trending_repositories_text_response = take_least_days_github_posts()
    trending_repositories = json.loads(trending_repositories_text_response)
    return trending_repositories['items'][:top_size]


def get_number_of_issues(repo_owner, repo_name):
    issues_answer = requests.get("https://api.github.com/repos/%s/%s/issues" % (repo_owner['login'], repo_name))
    json_issues_answer = json.loads(issues_answer.text)
    number_of_issues = len(json_issues_answer)
    return number_of_issues


def project_parser(projects_json_list):
    for project in projects_json_list:
        issues = get_number_of_issues(project['owner'], project['name'])
        yield project['html_url'], issues


if __name__ == '__main__':
    my_top_size = 20
    github_newest_projects = get_trending_repositories(my_top_size)
    print("Best GitHub Projects:")
    for link, issues in project_parser(github_newest_projects):
        print("%s : %s issues " % (link, issues))
