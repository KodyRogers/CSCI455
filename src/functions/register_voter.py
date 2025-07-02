###############################################
# Author: Kody Rogers
# Date: 6/27/2025
# Description: adds a new voter to the database
# Version: 1.0
###############################################

from psycopg2.extras import RealDictCursor

def action(curs: RealDictCursor, state, fname, mname, lname, ssn, party):

        if state.get('user') != None:
                user = state["user"]["first_name"]
                print(f"You are already signed in as {user}")
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
                curs.execute("INSERT INTO postgres.public.voters (first_name, middle_name, last_name, ssn, registered_at, party)" +
                            " VALUES (%s, %s, %s, %s, NOW(), %s)", (fname, mname, lname, ssn, party) ) 
                print(f"{fname} has been registered to vote!")
                return True

        return False