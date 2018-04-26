#database.py
import sys,shelve

def store_person(db):
    """
    Querry user for data and store it in the shelf object
    """

    pid = input('Enter unique Keywords: ')
    person = {}
    person['account_number'] = input('Enter account_number: ')
    person['password'] = input('Enter password: ')
    person['description'] = input('Enter description: ')

    db[pid] = person

def lookup_person(db):
    """
    Querry user for ID and desire field, and fetch the corresponding data from the shelf object
    """

    pid = input('Enter Keywords: ')
    db_n[pid] = db[pid]
    print_screen(db_n)


def print_screen(db):
    list_k = ['Keywords']
    list_1 = ['account_number']
    list_2 = ['password']
    list_3 = ['description']
    
    for k in db.keys():
        list_k.append(k)
        list_1.append(db[k]['account_number'])
        list_2.append(db[k]['password'])
        list_3.append(db[k]['description'])

    width_k = max_len(list_k)
    width_1 = max_len(list_1)
    width_2 = max_len(list_2)
    width_3 = max_len(list_3)

    margin = 2
    print('')
 
    print( '+' + '-' * ( margin + width_k + margin ) + '+'  + '-' * ( margin + width_1 + margin ) + '+' + '-' * ( margin + width_2 + margin ) + '+' + '-' * ( margin + width_3 + margin ) + '+')
    print( '|' + ' ' * margin + list_k[0] + ' ' * ( width_k + margin - len(list_k[0])) + '|' + ' ' * margin + list_1[0] + ' ' * ( width_1 + margin - len(list_1[0])) + '|' + ' ' * margin + list_2[0] + ' ' * ( width_2 + margin - len(list_2[0])) + '|' + ' ' * margin + list_3[0] + ' ' * ( width_3 + margin - len(list_3[0])) + '|')
    print( '+' + '-' * ( margin + width_k + margin ) + '+'  + '-' * ( margin + width_1 + margin ) + '+' + '-' * ( margin + width_2 + margin ) + '+' + '-' * ( margin + width_3 + margin ) + '+')
    
    for k in db.keys():
        ukw = k
        uaccount = db[k]['account_number']
        upassword = db[k]['password']
        udes = db[k]['description']
        print( '|' + ' ' * margin + ukw + ' ' * ( width_k + margin - len(ukw)) + '|' + ' ' * margin + uaccount + ' ' * ( width_1 + margin - len(uaccount)) + '|' + ' ' * margin + upassword + ' ' * ( width_2 + margin - len(upassword)) + '|' + ' ' * margin + udes + ' ' * ( width_3 + margin - len(udes)) + '|')
    print( '+' + '-' * ( margin + width_k + margin ) + '+'  + '-' * ( margin + width_1 + margin ) + '+' + '-' * ( margin + width_2 + margin ) + '+' + '-' * ( margin + width_3 + margin ) + '+')
    print('')
        
def max_len(li):
    return max([len(x) for x in li])

def print_help():
    print('')
    print('The available commands are: ')
    print('store : Stores information about a account number.')
    print('lookup: Looks up a account number from Keywords.')
    print('all   : Shows all account number.')
    print('quit  : Save changes and exit.')
    print('?     : Prints this message.')
    print('')

def enter_command():
    print('')
    cmd = input('Enter command ( ? for help ): ')
    cmd = cmd.strip().lower()
    return cmd

def main():
    database = shelve.open('\..\database.dat')
    try:
        while True:
            cmd = enter_command()
            if cmd == 'store':
                store_person(database)
            elif cmd == 'lookup':
                lookup_person(database)
            elif cmd == 'all':
                print_screen(database)
            elif cmd == '?':
                print_help()
            elif cmd == 'quit':
                return
    finally:
        database.close()

if __name__ == '__main__':main()
