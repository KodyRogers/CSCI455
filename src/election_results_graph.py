import psycopg2
import matplotlib.pyplot as plt
import pandas as pd

from os import path
from psycopg2.extras import RealDictCursor


CREDENTIALS_FILE = 'ssh.txt' if path.exists('ssh.txt') else '../ssh.txt'

def main():

    # get user/pass for db
    with open(CREDENTIALS_FILE) as f:
        username, password = [l.strip() for l in f.readlines()]

    # direct database connection (no SSH tunnel)
    params = {
        'database': 'postgres',           # replace with your actual database name
        'user': username,
        'password': password,
        'host': '34.123.152.151',         # public IP of your Cloud SQL instance
        'port': 5432                      # default PostgreSQL port
    }

    try:
        conn = psycopg2.connect(**params)
        curs = conn.cursor(cursor_factory=RealDictCursor)
        print("Database connection established")

        curs.execute(f'''
            WITH candidate_counts AS (
                SELECT candidate_id, COUNT(*) AS vote_count
                FROM votes
                GROUP BY candidate_id
            ),
            top_two AS (
                SELECT candidate_id
                FROM candidate_counts
                ORDER BY vote_count DESC
                LIMIT 2
            )
            SELECT 
                CASE
                    WHEN candidate_id IN (SELECT candidate_id FROM top_two) THEN CAST(candidate_id AS TEXT)
                    ELSE 'Other'
                END AS candidate_group,
                COUNT(*) AS votes
            FROM votes
            GROUP BY candidate_group;
        ''')
        out = curs.fetchall()
        candidate = {}

        voted = 0

        for i,row in enumerate(out):
            voter_id = row['candidate_group']

            voted += row['votes']

            if (voter_id != "Other"):
                curs.execute(f'''
                    SELECT * FROM postgres.public.voters WHERE voter_id = {voter_id};
                ''')
                result = curs.fetchone()
                candidate[i] = result['first_name'] + " " + result['last_name']
            else:
                candidate[i] = "Other"

        curs.execute(f'''
            Select Count(*) as total_count from postgres.public.voters
        ''')

        out = curs.fetchone()
        not_voted = out['total_count'] - voted

        # Pie chart data
        labels = ['Voted', 'Did Not Vote']
        sizes = [voted, not_voted]
        colors = ['#66b3ff', '#ff9999']
        explode = (0.05, 0.05)  # optional: separate both slices

        # Create the pie chart
        plt.figure(figsize=(6, 6))
        plt.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            colors=colors,
            explode=explode,
            shadow=True
        )
        plt.title(f"Voter Participation\nTotal: {voted + not_voted}")
        plt.axis('equal')  # Keep it a circle
        plt.show()

        #print(total)
        #sizes = [row['votes'] for row in out]



    except Exception as e:
        print(f"Connection failed: {e}")

    finally:
        if curs:
            curs.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    main()