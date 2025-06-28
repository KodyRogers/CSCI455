import psycopg2
from psycopg2.extras import RealDictCursor
from os import listdir, path
import importlib
from inspect import signature, Parameter

FUNCTIONS_DIR = './functions' if path.exists('./functions') else './src/functions'
CREDENTIALS_FILE = 'ssh.txt' if path.exists('ssh.txt') else '../ssh.txt'

def login(curs, name, password):
    pass

def test(curs):
    curs.execute('''
        SELECT NOW();
    ''')
    print(curs.fetchall())

def main():
    # import all user actions/functions
    actions = {}
    for fname in listdir(FUNCTIONS_DIR):
        if not fname.endswith('.py'):
            continue
        module_name = fname[:-3]
        module = importlib.import_module(f'functions.{module_name}')
        if not hasattr(module, 'action'):
            raise Exception(f'function module "{module_name}" missing required function "action"')
        actions[module_name] = module.action

    # get user/pass for db
    with open(CREDENTIALS_FILE) as f:
        username, password = [l.strip() for l in f.readlines()]

    # direct database connection (no SSH tunnel)
    params = {
        'database': 'postgres',           # replace with your actual database name
        'user': username,
        'password': password,
        'host': '34.123.152.151',         # public IP of your Cloud SQL instance
        'port': 5432                      # default PostgreSQL port
    }

    try:
        conn = psycopg2.connect(**params)
        curs = conn.cursor(cursor_factory=RealDictCursor)
        print("Database connection established")
        # this is used to store state data for the commands, like the user currently logged in
        state = {
            'user': None,
            'conn': conn
        }

        print('command list: ', ', '.join([a for a in actions]))

        while True:
            raw = input(': ')
            args = []
            for i, chunk in enumerate(raw.split('"')):
                if i & 0b1:
                    args.append(chunk)
                else:
                    if len(chunk.strip()) == 0:
                        continue
                    args += chunk.strip().split(' ')

            if args[0] in ['q', 'quit']:
                break
            elif args[0] in ['h', 'help']:
                print('command list: ', ', '.join([a for a in actions]))
            elif args[0] in actions:
                func = actions[args[0]]
                sig = signature(func)
                nargs = len(sig.parameters) - 2
                minargs = nargs - len([a for a in sig.parameters.values() if a.default != Parameter.empty])

                if not (minargs <= len(args) - 1 <= nargs):
                    if minargs == nargs:
                        print(f"Expected {nargs} arguments ({', '.join(list(sig.parameters.keys())[2:])}), given {len(args)-1}")
                    else:
                        print(f"Expected between {minargs} and {nargs} arguments, the last {nargs - minargs} are optional ({', '.join(list(sig.parameters.keys())[2:])}), given {len(args)-1}")
                    continue
                
                if func(curs, state, *args[1:]):
                    conn.commit()
            else:
                print('no such action exists')

    except Exception as e:
        print(f"Connection failed: {e}")

    finally:
        if curs:
            curs.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    main()