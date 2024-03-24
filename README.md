# tum-web-lab5

<b>Task.</b> Implement HTTP requesting via websokets. The program should implement at least the following CLI functionality:

    go2web -u <URL>         # make an HTTP request to the specified URL and print the response
    go2web -s <search-term> # make an HTTP request to search the term using your favorite search engine and print top 10 results
    go2web -h               # show this help

<b>How to test.</b> In order to build an executable you will need pyinstaller module:

    >> pip3 install pyinstaller
    >> pyinstaller --onefile go2web.py

In the <b>dist/</b> will be an executable with the same name as the script.

<b>Demo.</b> Below you may find a screen recorded demo of the program in action:

![demo.gif](./demo.gif)

<b>Additional stuff.</b> As you can see in the demo, Content negotiation and HTTP caching mechanisms were implemented. The program adequately reacts to responses in JSON format and records the previous requests so that if you request some URL for the second time, it pulls the data from the cache and does not request it for the second time.