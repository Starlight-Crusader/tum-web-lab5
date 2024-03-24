import sys
import warnings
from urllib.parse import quote
from functionality import http_get, get_response_to_leformat, search_response_to_leformat

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

warnings.filterwarnings("ignore", category=DeprecationWarning)

def main():
    if len(sys.argv) == 1 or sys.argv[1] == '-h':
        print("go2web -u <URL>          # make an HTTP request to the specified URL and print the response")
        print("go2web -s <search-term>  # make an HTTP request to search the term using your favorite search engine and print top 10 results")
        print("go2web -h                # show this help")
        
        return

    if sys.argv[1] == '-u':
        if len(sys.argv) != 3:
            print("Error: Missing URL argument")
            
            return
        
        url = sys.argv[2]
        print(get_response_to_leformat(http_get(url)), '\n')

    elif sys.argv[1] == '-s':
        if len(sys.argv) < 3:
            print("Error: Missing search words")
            return
        
        line = ' '.join(sys.argv[2:])
        print(search_response_to_leformat(http_get("https://www.google.com/search?q=" + quote(line))), '\n')

    else:
        print("Invalid option. Use '-h' for help.")

if __name__ == "__main__":
    main()
