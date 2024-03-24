import socket, ssl, json
from urllib.parse import urlparse
import bs4
import hashlib
from tinydb import Query, TinyDB

cache_file = "cache.json"
db = TinyDB(cache_file)

def hash_url(url):
    return hashlib.md5(url.encode()).hexdigest()

def cache_resp(url, resp_data):
    db.insert({'url': hash_url(url), 'resp_data': resp_data})

def check_cache(url):
    return db.contains(Query().url == hash_url(url))

def retrieve_cache(url):
    result = db.get(Query().url == hash_url(url))
    return result['resp_data'] if result else None

def get_response_to_leformat(response):
    if 'text/html' in response:
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
    elif 'application/json' in response:
        try:
            json_data = json.loads(response.split('\r\n\r\n', 1)[1])
            prettified_json = json.dumps(json_data, indent=4)
            return prettified_json
        except json.JSONDecodeError:
            return response
    else:
        return response

def search_response_to_leformat(response):
    soup = bs4.BeautifulSoup(response, 'html.parser')

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
    if check_cache(url):
        print("Retrieving cached response: ", hash_url(url), '\n')
        return retrieve_cache(url)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host, port, path = extract_url_data(url)
    print("Establishing websocket connection:", host, port, path, '\n')

    if port == 443:
        client_socket = ssl.wrap_socket(client_socket)

    try:
        client_socket.settimeout(2)
        client_socket.connect((host, port))

        request = f"GET {url} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        client_socket.send(request.encode())

        response = b""
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                response += data
            
            except socket.timeout:
                break

        resp_data = response.decode('utf-8', errors='ignore')
        cache_resp(url, resp_data)

        return resp_data
    
    finally:
        client_socket.close()