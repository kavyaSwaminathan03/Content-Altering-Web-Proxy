# Content-Altering-Web-Proxy
 An HTTP proxy server to modify web content

How to compile the Web proxy

The Web proxy is a simple python code which can be compiled in any environment that supports python, Like VS Code or IDLE.

How to configure the Web proxy

Open any web browser [I used Firefox] and change the network settings. 
1.	Select Manual Proxy Configuration
2.	Set HTTP Proxy as: 127.0.0.1 and port no as: 8080
   
Features that the proxy supports.
1.	Basic HTTP Request Handling (simple HTTP `GET` requests and fetch content from remote servers)
2.	Content Modification for HTML and Plain Text (proxy replaces occurrences of specific words like "Smiley" to "Trolly", "Stockholm" to "Linköping")
3.	Modifieds embedded or linked JPG images of smiley to display a troll image.
4.	Non-Modifying Behaviour for Other Content Types (the proxy forwards this content unchanged to the client)
5.	Error Handling (catches exceptions during request processing, and ensures that the connection is properly closed in the event of an error)
   
The proxy is tested on the following HTTP pages

1.	A simple ASCII text file: http://zebroid.ida.liu.se/fakenews/test1.txt
2.	A looong ASCII text file: http://zebroid.ida.liu.se/fakenews/test2.txt
3.	A simple HTML file: http://zebroid.ida.liu.se/fakenews/test3.html
4.	An HTML file with link to a photo: http://zebroid.ida.liu.se/fakenews/test4.html
5.	An HTML file with embedded photos: http://zebroid.ida.liu.se/fakenews/test5.html

