###############################################
# Author: Kody Rogers
# Date: 7/22/2025
# Description: Ends the Election 
# Version: 1.0
###############################################

from psycopg2.extras import RealDictCursor

def action(curs: RealDictCursor, state, electionName):

    if state['user'] == None:
        print("You are currently not logged in!")
        return False
    
    if state['user']['is_admin'] == False:
        print("You need to be an Administrator to use this command!")
        return False

    curs.execute(f'''
        SELECT * FROM postgres.public.elections WHERE name = '{electionName}';
    ''')
    out = curs.fetchone()

    if (out == None):
        print("Election does not exist!")
        return False

    election_id = out['election_id']

    curs.execute(f'''
        UPDATE elections SET is_active = FALSE WHERE election_id = '{election_id}';
    ''')
    print(f"The Election: '{electionName}' is now closed!")
    return True