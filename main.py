import requests
from bs4 import BeautifulSoup


# Base url
base_url = "https://github.com"

# Making a GET request
fork_url = "https://github.com/frdmn/docker-speedtest-grafana/network/members"

# List of url forks
forks = []

response = requests.get(fork_url)
# check status code for response received
if response.status_code == 400 or response.status_code == 500:
    print("Error al ingresar al sitio web")
    exit()

# Parsing the HTML
soup = BeautifulSoup(response.content, 'html.parser')
# Finding by id
divs = soup.find('div', id= 'network')
anchors = divs.find_all('a', class_='')
for i in anchors:
    if len(i.get('href').split("/")) > 2:
        forks.append(i.get('href'))

repos = []
progress = ""
for url in forks:
    response_fork = requests.get(base_url + url)
    if response_fork.status_code == 400 or response_fork.status_code == 500:
        print("Error al ingresar al fork: " + url)
        continue
    soup_fork = BeautifulSoup(response_fork.content, 'html.parser')
    div_fork = soup_fork.find('div', class_='js-details-container')
    commits_value = div_fork.find('strong').text
    if len(repos) == 0:
        repos.append({"url": base_url+url, "commits": int(commits_value)})
    else:
        for i in repos:
            if int(commits_value) >= i["commits"]:
                # repos.append({"url": base_url+url, "commits": int(commits_value)})
                i["url"] = base_url+url
                i["commits"] = int(commits_value)
            progress += "."
            print(progress)

print(repos)                
