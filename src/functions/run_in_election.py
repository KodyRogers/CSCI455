###############################################
# Author: Kody Rogers
# Date: 7/1/2025
# Description: Creates Elections
# Version: 1.0
###############################################
from psycopg2.extras import RealDictCursor

def action(curs: RealDictCursor, state: dict, electionName):
    

    if (state.get('user') == None):
        print("You are not logged in!")
        return False
    
    if (state['user']['is_admin'] == True):
        print("Admin can not run in the election!")
        return False
    
    voter_id = state['user']['voter_id']
    user = state['user']

    curs.execute(f'''
            SELECT election_id FROM postgres.public.elections WHERE name = '{electionName}';
    ''')

    out = curs.fetchone()
    if (out == None):
        print("No election with that name exist!")
        return False
    election_id = out['election_id']

    curs.execute(f'''
            SELECT * FROM postgres.public.candidates WHERE voter_id = '{voter_id}' AND election_id = '{election_id}';
    ''')
    out = curs.fetchone()

    if (out == None):
        curs.execute("INSERT INTO postgres.public.candidates (voter_id, election_id)" +
                    " Values (%s, %s)", (voter_id, election_id))
        
        print(f"Voter {user["first_name"]} {user["last_name"]} has been nominated for election {electionName}!")
        return True
    
    print ("User is already running in this election")
    return False