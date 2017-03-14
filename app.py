import os, requests, json, Queue, operator

class Github:
    base_url_user = "https://api.github.com/search/users?q=location:"
    is_from_colombia = {}
    auth = ()
    best_repos = Queue.PriorityQueue()
    best_repos2 = {}
    need = 10
    max_page = 1000

    def __init__ (self, country, username, password):
        Github.base_url_user = Github.base_url_user + country
        Github.auth = (username, password)

    def fetch_users (self):
        tmp_url = Github.base_url_user + '&page='
        for page in range (1, Github.max_page):
            req = requests.get(tmp_url + str(page), auth = Github.auth)
            if (req.ok):
                ans = json.loads(req.text or req.content)
                items = ans['items']

                for cur in items:
                    Github.is_from_colombia[str(cur['login'])] = True
            else:
                break

    def fetch_repos (self, user):
        url = "https://api.github.com/users/" + user + "/repos?type=collaborator"
        req = requests.get(url, auth = Github.auth)
        if (req.ok):
            ans = json.loads(req.text or req.content)

            for cur in ans:
                tot = Github.best_repos.qsize()
                other = (cur['stargazers_count'], str(cur['html_url']))

                key = str(cur['html_url'])
                if (Github.best_repos2.has_key(key)):
                    Github.best_repos2[key] += 1
                else:
                    Github.best_repos2[key] = 1

                if (tot < Github.need):
                    Github.best_repos.put(other)
                    continue

                mmin = Github.best_repos.get()

                if (int(mmin[0]) < int(other[0])):
                    mmin = other

                Github.best_repos.put(mmin)

    def print_ans (self):
        q = Github.best_repos
        arr = []
        while not q.empty():
            cur = q.get()
            arr.append(cur)

        print ("Top 10 repositories")
        l = len(arr)
        for i in range (0, l):
            print (arr[l - i - 1][0], arr[l - i - 1][1])

        print ("------")

        # TODO: Fix top 10 repositories with more Colombian collaborators
        #       - unexpected results
'''
        sorted_repo = sorted(Github.best_repos2.items(), key = operator.itemgetter(1))
        l = len(sorted_repo) - 1
        cnt = 10
        while cnt > 0:
            print (sorted_repo[l][0], sorted_repo[l][1])
            l -= 1
            cnt -= 1
'''

username = os.environ['GH_USER']
password = os.environ['GH_PASSWORD']

query = Github("colombia", username, password)
query.fetch_users()

for username in query.is_from_colombia:
    query.fetch_repos(username)

query.print_ans()
