###############################################
# Author: Kody Rogers
# Date: 6/27/2025
# Description: logs the user in
# Version: 1.0
###############################################

from psycopg2.extras import RealDictCursor

def action(curs: RealDictCursor, state, firstname, lastname, l4ssn):
    curs.execute(f'''
        SELECT * FROM postgres.csci455.voters WHERE first_name = '{firstname}' AND last_name = '{lastname}';
    ''')
    out = curs.fetchall()
    print(out)
    #print(f'you tried to login with {firstname}, {l4ssn}')

    if len(out) == 0:
        print(f'Incorrect Name')
    elif l4ssn != out[0]['ssn'][-4:]:
        print(f'Incorrect SSN digits')
    else:
        # success
        print(f"Successfully logged in as: '{firstname} {lastname}'")
        state['user'] = out[0]

        # return true to commit changes
        return True

    # Don't commit anything on incorrect login
    return False