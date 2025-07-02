###############################################
# Author: Kody Rogers
# Date: 6/30/2025
# Description: logs the user in
# Version: 1.0
###############################################

from psycopg2.extras import RealDictCursor

def action(curs: RealDictCursor, state, username, password):


    if state.get('user') != None:
        print('Currently logged in')
        return False

    curs.execute(f'''
        SELECT * FROM postgres.public.admins WHERE username = '{username}' AND password = '{password}';
    ''')
    out = curs.fetchall()
    print(out)

    if len(out) == 0:
        print(f'Incorrect username')
    elif password != out[0]['password']:
        print(f'Incorrect password')
    else:
        # success
        print(f"Successfully logged in as: '{username}'")
        state['user'] = out[0]

        # return true to commit changes
        return True

    # Don't commit anything on incorrect login
    return False