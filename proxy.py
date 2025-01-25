import socket
import re

def start_proxy(port=8080):
    # Create a socket that listens (proxy server)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', port))
    server.listen(5)
    print(f"Proxy is ready on port {port}!")

    while True:
        client, address = server.accept()
        print(f"{address} is talking to the proxy!")
        handle_request(client)

def handle_request(client):
    try:
        request = client.recv(4096).decode('utf-8')
        if not request:
            print("No request received.")
            client.close()
            return
            
        lines = request.split('\n')
        if lines:
            print("\nRequested task:\n", lines[0])
            # Pass this request to our content modifier
            content_modifier(lines[0], client)
    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        client.close()

def content_modifier(request_line, client):
    try:
        # Parse the request to get the URL
        url = request_line.split(' ')[1]
        
        # Extract the host and path from the URL
        host = url.split('/')[2]
        path = '/'.join(url.split('/')[3:])  # Extracting the path

        print(f"Connecting to {host}!")

        # Create a new socket to talk to the web server
        web_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        web_socket.connect((host, 80))

        # Construct the full HTTP request
        request_to_send = f"GET /{path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        web_socket.sendall(request_to_send.encode())

        # Fetch the response from the web server
        response = b''
        while True:
            part = web_socket.recv(4096)  # Use a buffer size of 4096 bytes
            if len(part) == 0:
                break
            response += part

        # Split the headers and body
        response_parts = response.split(b'\r\n\r\n', 1)
        if len(response_parts) != 2:
            print("Response format invalid!")
            return
        response_header = response_parts[0]
        response_body = response_parts[1]
        response_header_decoded = response_header.decode('utf-8', errors='ignore')

        # Detect content type and modify based on type
        if 'Content-Type: text/plain' in response_header_decoded:
            # If it's a plain text file
            body = response_body.decode('utf-8', errors='ignore')
            body = body.replace('Smiley', 'Trolly').replace('Stockholm', 'Linköping')
            altered_response = response_header_decoded + '\r\n\r\n' + body
            client.sendall(altered_response.encode('utf-8'))
        
        elif 'Content-Type: text/html' in response_header_decoded:
            # If it's an HTML file
            body = response_body.decode('utf-8', errors='ignore')

            # Function to replace text content between HTML tags
            def replace_text_content(match):
                text = match.group(1)
                if not re.search(r'<.*?>', text):  # Check if there are no HTML tags inside the content
                    return text.replace('Smiley', 'Trolly').replace('Stockholm', 'Linköping')
                return text

            # Replace text between HTML tags
            altered_body = re.sub(r'>([^<]+)<', lambda m: f'>{replace_text_content(m)}<', body)

            # Replace the src attribute for Smiley image (embedded img)
            altered_body = re.sub(r'src="(.*?smiley\.jpg)"', r'src="http://zebroid.ida.liu.se/fakenews/trolly.jpg"', altered_body)
            
            # Replace the href attribute for Smiley image (link to image)
            altered_body = re.sub(r'href="(.*?smiley\.jpg)"', r'href="http://zebroid.ida.liu.se/fakenews/trolly.jpg"', altered_body)
            
            # Combine the header and modified body
            altered_response = response_header_decoded + '\r\n\r\n' + altered_body

            # Send the modified response
            client.sendall(altered_response.encode('utf-8'))

        else:
            # For non-text responses, send unmodified data
            client.sendall(response)

    except Exception as e:
        print(f"Error during content modification: {e}")
    finally:
        web_socket.close()

# Start the proxy server
if __name__ == "__main__":
    start_proxy()
