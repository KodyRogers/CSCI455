from datetime import date
from psycopg2.extras import RealDictCursor

def action(curs: RealDictCursor, state, electionName, candidateID):

    if state['user'] == None:
        print("You are currently not logged in to vote!")
        return False
    if state['user']['is_admin'] == True:
        print("You can not vote as an Admin!")
        return False

    userID = state['user']['voter_id']

    # Gets the ElectionID to be used in voting
    curs.execute(f'''
        SELECT election_id FROM postgres.public.elections WHERE name = '{electionName}';
    ''')
    out = curs.fetchone()
    if (out == None):
        print("This election does not exist!")
        return False
    
    # Checks if election has ended
    electionDate = out['date']
    electionDate = electionDate.strftime("%Y-%m-%d")
    if(electionDate < date.today()):
        print("This election has already ended!")
        return False
    
    electionID = out['election_id']

    # Makes sure candidate is running in the election
    curs.execute(f'''
        SELECT * FROM postgres.public.candidates WHERE voter_id = '{candidateID}' AND election_id = '{electionID}';
    ''')
    out = curs.fetchone()
    if (out == None):
        print("This person is not running in this election")
        return False
    
    # Gets Candidates information
    curs.execute(f'''
        SELECT * FROM postgres.public.voters WHERE voter_id = '{candidateID}';
    ''')
    out = curs.fetchone()
    candidateInfo = out

    #Checks if already voted
    curs.execute(f'''
        SELECT * FROM postgres.public.votes WHERE voter_id = '{userID}' AND election_id = '{electionID}';
    ''')
    out = curs.fetchone()
    if (out != None):
        print("You have already voted in this election!")
        return False
    else:
        curs.execute("INSERT INTO postgres.public.votes (voter_id, candidate_id, election_id, voted_at)" +
                 " Values (%s, %s, %s, NOW())", (userID, candidateID, electionID))
        print(f"You have voted in the Election: {electionName}, for Candidate: {candidateInfo["first_name"]} {candidateInfo["last_name"]}")
        return True

