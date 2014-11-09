import sqlite3
db_filename = '/Users/shumake/Desktop/Indeed_data/db.sqlite3'
with sqlite3.connect(db_filename) as conn:
    cursor = conn.cursor()
    cursor.execute("""
    SELECT DISTINCT date FROM search WHERE term = "data+scientist"
    """)
    date_of_search = cursor.fetchone()[0]
    cursor.execute("""
    SELECT COUNT(DISTINCT link) FROM links WHERE search_id = 1
    """)
    num_ads = cursor.fetchone()[0]

    
    msg =  "The search was conducted on {0} and returned {1} distinct ads."
    msg = msg.format(date_of_search,num_ads)
    print msg
    
    cursor.execute("""
    SELECT
    LOWER(word) AS 'Word', SUM(count) AS 'Count'
    FROM DataScientist
    GROUP BY LOWER(word)
    ORDER BY SUM(count) DESC
    """)
    