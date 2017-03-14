import os, requests, json, Queue

class Github:
    base_url_user = "https://api.github.com/search/users?q=location:"
    is_from_colombia = {}
    best_repos = Queue.PriorityQueue();
    need = 10
    max_page = 10

    def __init__ (self, country):
        Github.base_url_user = Github.base_url_user + country

    def fetch_users (self):
        tmp_url = Github.base_url_user + '&page=';
        for page in range(1, Github.max_page):
            req = requests.get(tmp_url + str(page))
            if (req.ok):
                ans = json.loads(req.text or req.content)
                items = ans['items'];

                for cur in items:
                    Github.is_from_colombia[str(cur['login'])] = True
            else:
                break

    def fetch_repos (self, user):
        url = "https://api.github.com/users/" + user + "/repos?type=collaborator"
        req = requests.get(url)
        if (req.ok):
            ans = json.loads(req.text or req.content)
            # TODO
            # - Iterate over repositories and mantains in a priority queue the
            #   best 10 repositories, order by 'stargazers_count'

        else:
            print "Error: ", req.status_code

    def print_ans (self):
        q = Github.best_repos
        while not q.empty():
            print q.get(),


query = Github("colombia")
query.fetch_users()

for username in query.is_from_colombia:
    query.fetch_repos(username)

query.print_ans;
