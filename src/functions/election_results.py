###############################################
# Author: Johnathan Green + Kody Rogers
# Date: 7/22/2025
# Description: Gets the Results of a finished Election
# Version: 1.1
###############################################

from psycopg2.extras import RealDictCursor

def action(curs: RealDictCursor, state, electionName):

    if state['user'] == None:
        print("You are currently not logged in!")
        return False
    

    # Gets the ElectionID to be used in voting
    curs.execute(f'''
        SELECT * FROM postgres.public.elections WHERE name = '{electionName}';
    ''')
    out = curs.fetchone()
    if (out == None):
        print("This election does not exist!")
        return False
    
    # Checks if election has ended
    electionActive = out['is_active']
    if(electionActive):
        print("This election has not ended yet")
        return False
    
    election_id = out['election_id']

    curs.execute(f'''
        SELECT * FROM postgres.public.candidates WHERE election_id = '{election_id}';
    ''')
    out = curs.fetchall()

    if len(out) == 0:
        print("No user running in that election")
        return False
    
    print(f"Results of votes for {electionName}")
    print("=============================================")

    for row in out:
        candidate = row['voter_id']
        curs.execute(f'''
            SELECT * FROM postgres.public.voters WHERE voter_id = '{candidate}';
        ''')
        candidateInfo = curs.fetchone()
        print(f"CandidateID: '{candidateInfo["voter_id"]}', Name: '{candidateInfo["first_name"]}' '{candidateInfo["middle_name"][0]}' '{candidateInfo["last_name"]}', Party: '{candidateInfo["party"]}'")
        curs.execute(f" SELECT * FROM postgres.public.votes WHERE election_id = '{election_id}' AND candidate_id = '{candidate}'")
        votes = curs.fetchall()
        print(f"Votes: '{len(votes)}'")
        print("--------------------------------------")
