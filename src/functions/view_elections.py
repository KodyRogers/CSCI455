###############################################
# Author: Johnathan Green & Kody Rogers
# Date: 7/01/2025
# Description: displays all running elections + past elections
# Version: 1.1
###############################################

from psycopg2.extras import RealDictCursor

def action(curs: RealDictCursor, state: dict):
  
  
  curs.execute('''
      SELECT * FROM postgres.public.elections WHERE DATE > CURRENT_DATE AND is_active = true
  ''')

  print("Ongoing Elections")
  print("=================")

  elections = curs.fetchall()
  if (len(elections) == 0):
    print("Could not find any running elections")
  else:
    for row in elections:
      print(f"Election Name: {row['name']}, Status Ongoing Until: {row['date']}, Election Type: {row['type']}")
      
  curs.execute('''
      SELECT * FROM postgres.public.elections WHERE DATE < CURRENT_DATE OR is_active = false;
  ''')
  elections = curs.fetchall()

  print("\nPast Elections")
  print("=================")
  
  #elections = curs.fetchall()
  if (len(elections) == 0):
    print("Could not find any past elections")
  else:
    for row in elections:
      print(f"Election Name: {row['name']}, Status Ongoing Until: {row['date']}, Election Type: {row['type']}")

  return False
#SELECT name, party, position FROM candidates WHERE election_id = 1
#SELECT * FROM postgres.csci455.elections