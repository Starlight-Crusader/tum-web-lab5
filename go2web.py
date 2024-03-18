import socket
from urllib.parse import urlparse
import bs4
import os
import sys

def extract_url_data(url):
    parsed_url = urlparse(url)
    
    return parsed_url.netloc, 80, parsed_url.path

def http_get_req(url):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host, port, path = extract_url_data(url)

    print(host, port, path)

    try:
        client_socket.connect((host, port))

        request = f"GET {url} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        client_socket.send(request.encode())

        response = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            response += data

            headers = response.split(b"\r\n\r\n")[0].decode().splitlines()
            for header in headers:
                if header.startswith("Content-Length"):
                    content_length = int(header.split(": ")[1])
                    break

            if content_length is not None and len(response) >= content_length:
                break

        return response.decode()
    
    finally:
        client_socket.close()

while (True):
    command = input(">>> ")

    if command[:9] == "go2web -h":
        print("go2web -u <URL>          # make an HTTP request to the specified URL and print the response")
        print("go2web -s <search-term>  # make an HTTP request to search the term using your favorite search engine and print top 10 results")
        print("go2web -h                # show this help")
        print("go2web -c                # clear the terminal")
        print("go2web -e                # exit this CLI\n")
    elif command[:9] == "go2web -u":
        response = http_get_req(command[10:])
        print(bs4.BeautifulSoup(response).text + "\n")
    elif command[:9] == "go2web -c":
        os.system("clear")
    elif command[:9] == "go2web -e":
        sys.exit()
    else:
        print("Invalid syntax!\n")


# ex_url = "http://www.columbia.edu/~fdc/sample.html"