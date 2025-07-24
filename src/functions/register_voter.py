###############################################
# Author: Kody Rogers
# Date: 6/27/2025
# Description: adds a new voter to the database
# Version: 1.0
###############################################

from psycopg2.extras import RealDictCursor

def action(curs: RealDictCursor, state, fname, mname, lname, ssn, party):

        if state.get('user') == None:
                print("You have not logged in yet!")
                return False

        if (state['user']['is_admin'] == False):
                print("You are not signed in as an admin!")
                return False
        
        if len(ssn) != 11:
                print(f"Social Security is not valid! Format XXX-XX-0000")
                return False

        if not ssn.startswith('XXX-XX-') and ssn[7:].isdigit():
                print(f"Social Security is not valid! Format XXX-XX-0000")
                return False

        curs.execute(f'''
                SELECT * FROM postgres.public.voters WHERE ssn = '{ssn}';
                     ''')
        out = curs.fetchall()
        #print(out)      #used for testing output
        
        if (len(out) != 0):
                print("This SSN is already in use!")
        else:
                
                curs.execute(f'''
                        SELECT MAX(voter_id) FROM postgres.public.voters;
                ''')
                next_id = curs.fetchone()['max'] + 1
        
                curs.execute("INSERT INTO postgres.public.voters (voter_id, first_name, middle_name, last_name, ssn, registered_at, party)" +
                            " VALUES (%s, %s, %s, %s, %s, NOW(), %s)", (next_id, fname, mname, lname, ssn, party) ) 
                print(f"{fname} has been registered to vote!")
                return True

        return False