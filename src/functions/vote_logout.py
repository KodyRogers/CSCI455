###############################################
# Author: Kody Rogers
# Date: 6/30/2025
# Description: logs the user in
# Version: 1.0
###############################################

from psycopg2.extras import RealDictCursor

def action(curs: RealDictCursor, state: dict):
  if state.get('user') == None:
    print('Not currently logged in')
  else:
    print('Successfully logged out')

  state['user'] = None