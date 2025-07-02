###############################################
# Author: Kody Rogers
# Date: 6/27/2025
# Description: views voter info
# Version: 1.0
###############################################

from psycopg2.extras import RealDictCursor

def action(curs: RealDictCursor, state):

    if state.get('user') == None:
        print('Not currently logged in')
        return False
    
    if (state['user']['is_admin'] == True):
        print("You are currently signed in as an admin and can't view user information!")
        return False
    
    user = state['user']

    print(f"{user['first_name']} {user['middle_name']} {user['last_name']} {user['ssn'][-4:]} {user['party']}" )