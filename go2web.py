import socket, ssl, warnings
from urllib.parse import urlparse, quote
import bs4

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

warnings.filterwarnings("ignore", category=DeprecationWarning)

def html_response_to_plain_text(response):
    html_content = response[response.find("\r\n\r\n") + 4:]
    soup = bs4.BeautifulSoup(html_content, 'html.parser')
    
    contents = []
    
    for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        if tag.name.startswith('h'):
            contents.append('\n\n\n')
        else:
            contents.append('\n\n')

        contents.append(tag.get_text(strip=True))
    
    return ''.join(contents)

def search_response_to_le_foramt(response):
    html_content = response[response.find("\r\n\r\n") + 4:]
    soup = bs4.BeautifulSoup(html_content, 'html.parser')

    headers = [div.get_text(strip=True) for div in soup.select('div.BNeawe.vvjwJb')]
    urls = [a.get('href') for a in soup.select('a[data-ved^="2ahUK"]')]
    cleaned_urls = [href.split("/url?q=")[-1].split("&")[0] if "/url?q=" in href else href for href in urls]

    result = ''
    for i in range(len(headers)):
        result = result + str(i+1) + ". " + headers[i] + '\n' + cleaned_urls[i] + "\n\n"

    return result

def extract_url_data(url):
    parsed_url = urlparse(url)

    port = None
    if parsed_url.scheme == "https":
        port = 443
    elif parsed_url.scheme == "http":
        port = 80
    
    return parsed_url.netloc, port, parsed_url.path

def http_get(url):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host, port, path = extract_url_data(url)
    print(host, port, path, '\n')

    try:
        ssl_client_socket = ssl.wrap_socket(client_socket)
        ssl_client_socket.settimeout(2)
        ssl_client_socket.connect((host, port))

        request = f"GET {url} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        ssl_client_socket.send(request.encode())

        response = b""
        while True:
            try:
                data = ssl_client_socket.recv(1024)
                if not data:
                    break
                
                response += data
            
            except socket.timeout:
                break

        return response.decode('utf-8', errors='ignore')
    
    finally:
        ssl_client_socket.close()

while (True):
    command = input(">>> ")

    if command[:9] == "go2web -h":
        print()
        print("go2web -u <URL>          # make an HTTP request to the specified URL and print the response")
        print("go2web -s <search-term>  # make an HTTP request to search the term using your favorite search engine and print top 10 results")
        print("go2web -h                # show this help")
    elif command[:9] == "go2web -u":
        print(html_response_to_plain_text(http_get(command[10:])), '\n')
    elif command[:9] == "go2web -s":
        print(search_response_to_le_foramt(http_get("https://www.google.com/search?q=" + quote(command[10:]))))
    else:
        print("Invalid syntax!\n")