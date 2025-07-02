###############################################
# Author: Kody Rogers
# Date: 7/2/2025
# Description: Views all running Candidates for
#              a given election
# Version: 1.0
###############################################
from psycopg2.extras import RealDictCursor

def action(curs: RealDictCursor, state: dict, electionName):
    

    curs.execute(f'''
            SELECT election_id FROM postgres.public.elections WHERE name = '{electionName}';
    ''')
    out = curs.fetchone()
    if (out == None):
        print("No election with that name exist!")
        return False
    election_id = out['election_id']


    curs.execute(f'''
        SELECT * FROM postgres.public.candidates WHERE election_id = '{election_id}';
    ''')
    out = curs.fetchall()

    if len(out) == 0:
        print("No user running in that election")
        return False
    
    print(f"List of Candidates running in {electionName}")
    print("=============================================")

    for row in out:
        candidate = row['voter_id']
        curs.execute(f'''
            SELECT * FROM postgres.public.voters WHERE voter_id = '{candidate}';
        ''')
        candidateInfo = curs.fetchone()
        print(f"Name: {candidateInfo['first_name']} {candidateInfo['middle_name'][0]} {candidateInfo['last_name']}, Party: {candidateInfo['party']}")

    return False  
