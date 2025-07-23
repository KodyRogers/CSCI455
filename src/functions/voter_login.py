###############################################
# Author: Kody Rogers
# Date: 7/2/2025
# Description: logs the user in
# Version: 1.0
###############################################

from psycopg2.extras import RealDictCursor

def action(curs: RealDictCursor, state, firstname, lastname, l4ssn):

    if state.get('user') != None:
        print('Currently logged in')
        return False


    if l4ssn.isdigit() == False:
        print("invalid ssn")
        return False

    curs.execute(f'''
        SELECT * FROM postgres.public.voters WHERE first_name = '{firstname}' AND last_name = '{lastname}';
    ''')
    out = curs.fetchall()
    #print(out) #Used for testing
    #print(f'you tried to login with {firstname}, {l4ssn}')

    if len(out) == 0:
        print(f'Incorrect Name')
    else: 
        for row in out:
            if row['ssn'][-4:] == l4ssn:
                print(f"Successfully logged in as: '{firstname} {lastname}'")
                state['user'] = row
                # return true to commit changes
                return True
            print("incorrect ssn digits")

    # Don't commit anything on incorrect login
    return False