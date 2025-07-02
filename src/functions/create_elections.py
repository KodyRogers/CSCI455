###############################################
# Author: Kody Rogers
# Date: 7/1/2025
# Description: Creates Elections
# Version: 1.0
###############################################
from psycopg2.extras import RealDictCursor

def action(curs: RealDictCursor, state: dict, electionName, date, electionType):
    
    if state.get('user') == None:
        print("You have not logged in yet!")
        return False

    if (state['user']['is_admin'] == False):
        print("You are not signed in as an admin!")
        return False

    curs.execute(f'''
        SELECT * from postgres.public.elections WHERE name = '{electionName}'
    ''')

    out = curs.fetchall()
    print("test")

    if (len(out) != 0):
        print("A election with this name already exist!")
        return False
    

    curs.execute("INSERT INTO postgres.public.elections (name, date, type)" +
                 " Values (%s, %s, %s)", (electionName, date, electionType))
    
    print(f"Election {electionName} has been added successfully!")
    return True