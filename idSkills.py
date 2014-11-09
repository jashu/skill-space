# Generate/update a list of job skills by crawling public LinkedIn profiles.
# This will be used to identify what terms in job ads correspond to skills. 

import requests,time
from bs4 import BeautifulSoup

goal = 150 #Number of new skills to add on this run.
        
def getNextURL(bs):
    next_url = None
    urls = bs.find_all('div', 'insights-browse-map')
    if urls:
        urls = urls[0].find_all('a','browse-map-photo')
        for url in urls:
            temp = url['href']
            temp = temp[:temp.find('?')]
            if temp and temp not in visited_urls:
                seed_urls.add(temp)
    if seed_urls:
        next_url = seed_urls.pop()
        visited_urls.add(next_url)
    return next_url

#Load data.
f = open('visitedURL.txt','r')
temp = f.read().splitlines()
f.close()
visited_urls = set(temp)

f = open('skillsList.txt','r')
temp = f.read().splitlines()
f.close()
skillset = set(temp)

f = open('seedURL.txt', 'r')
temp = f.read().splitlines()
seed_urls = set(temp)

#Initialize variables.
init_size = len(skillset)
old_size = init_size
global_increase = 0
local_increase = 0
url = seed_urls.pop()
visited_urls.add(url)

#Scrape skills.
while global_increase < goal and url:
    wait = local_increase*10+10
    time.sleep(wait)
    print "Scraping " + url
    response = requests.get(url)
    bs = BeautifulSoup(response.content)
    skills = bs.find_all('span','endorse-item-name-text')
    for skill in skills:
        try: skillset.add(str(skill.next))
        except UnicodeEncodeError: next
    new_size = len(skillset)
    global_increase = new_size - init_size
    local_increase = new_size - old_size
    old_size = new_size
    print "Added {0} new skills.".format(local_increase)
    print "{0} links explored.".format(len(visited_urls))
    print "{0} links to go.".format(len(seed_urls))
    url = getNextURL(bs)

print "Finished with a total of {0} new skills.".format(global_increase)

#save list of skills
f = open('skillsList.txt','w')
for skill in skillset:
    f.write(skill)
    f.write('\n')
f.close()

#save unvisited urls for use in the next run
if seed_urls:
    f = open('seedURL.txt', 'w')
    for url in seed_urls:
        f.write(url)
        f.write('\n')
    f.close()
else:
    print "Ran out of seed URLs."

#save visited urls to exclude in the next run
f = open('visitedURL.txt', 'w')
for url in visited_urls:
    f.write(url)
    f.write('\n')
f.close()