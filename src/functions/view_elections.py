###############################################
# Author: Johnathan Green
# Date: 7/01/2025
# Description: displays all elections and candidates
# Version: 1.0
###############################################

from psycopg2.extras import RealDictCursor

def action(curs: RealDictCursor, state: dict):
  if state.get('user') == None:
    print('Not currently logged in')
    return
  curs.execute('''
      SELECT * FROM postgres.csci455.elections
  ''')
  elections = curs.fetchall()
  #print(curs.fetchall())
  for row in elections:
    election_id = row[0]
    print(f"{row[1]} on {row[2]} [{row[3]}]")
    curs.execute(f'''
        SELECT name, party, position FROM postgres.csci455.candidates WHERE election_id = {election_id}
    ''')
    candidates = curs.fetchall()
    for candidate in candidate:
      print(f"\t{candidate[0]} ({candidate[1]} - {candidate[2]})")



#SELECT name, party, position FROM candidates WHERE election_id = 1
#SELECT * FROM postgres.csci455.elections