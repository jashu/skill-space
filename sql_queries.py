##Create a Python nested dictionary:
##First key is job title that looks up a dictionary of job skills for that 
##job title, that looks up the word count for that job skill in job ads.


import sqlite3, pickle
from collections import OrderedDict
db_filename = '/Users/shumake/Desktop/Indeed_data/db.sqlite3'

f = open('skillsList.txt','r')
job_skills = f.read().splitlines()
f.close()
for i in range(0,len(job_skills)):
    job_skills[i] = job_skills[i].split('.')[0].lower()
    job_skills[i] = job_skills[i].split(',')[0]
    job_skills[i] = job_skills[i].split('&')[0]
    job_skills[i] = job_skills[i].split('/')[0]
    
        
generate_query = lambda job: """
SELECT LOWER(word), SUM(count)
FROM
(SELECT word, count
FROM data_collector_results AS Results
JOIN data_collector_search AS Search
ON Results.search_id = Search.id
WHERE term = '{0}')
GROUP BY LOWER(word)
ORDER BY SUM(count) DESC
""".format(job)
        
with sqlite3.connect(db_filename) as conn:
    cursor = conn.cursor()
    cursor.execute("""
    SELECT DISTINCT term FROM search
    """)
    skill_space = {}
    
    for job in cursor.fetchall():
        skill_space[job[0]] = {}
    for job in skill_space.keys():
        print 'Working on ' + job
        cursor.execute(generate_query(job))
        word_counts = {}
        for word in cursor.fetchall():
            word_counts[word[0]] = word[1]
        for skill in job_skills:
            if skill in word_counts:
                skill_space[job][skill] = word_counts[skill]
            else:
                skill_space[job][skill] = 0
                

sorted_by_skill = {jt:OrderedDict(sorted(sk.items(),key = lambda t: t[1],\
reverse=True))  for jt, sk in skill_space.items()}

try:
    pickle.dump(sorted_by_skill,open('skill_space.p','w'))
except Exception as e:
    print '{0}, writing default'.format(e)
    pickle.dump(skill_space,open('skill_space.p','w'))
