import json
import socket

def send_request(socket, request):
    # LSP requires the content length in headers
    content = json.dumps(request)
    headers = f"Content-Length: {len(content)}\r\n\r\n"
    socket.sendall((headers + content).encode('utf-8'))

def receive_response(socket):
    # Read headers
    headers = ''
    while '\r\n\r\n' not in headers:
        headers += socket.recv(1).decode('utf-8')

    # Extract content length from headers
    content_length = int(headers.split('Content-Length: ')[1].split('\r\n')[0])
    
    # Read the content
    return json.loads(socket.recv(content_length).decode('utf-8'))

def get_semantic_tokens(file_path, language_server_address):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to the language server
        sock.connect(language_server_address)

        # Initialize the language server
        send_request(sock, {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "processId": None,
                "rootUri": None,
                "capabilities": {},
            }
        })
        print("Initialization response:", receive_response(sock))

        # Open the document
        send_request(sock, {
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {
                "textDocument": {
                    "uri": f"file://{file_path}",
                    "languageId": "python",
                    "version": 1,
                    "text": open(file_path).read()
                }
            }
        })

        # Request semantic tokens
        send_request(sock, {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "textDocument/semanticTokens/full",
            "params": {
                "textDocument": {
                    "uri": f"file://{file_path}",
                }
            }
        })
        return receive_response(sock)

# Example usage
file_path = "/path/to/your/code.py"
language_server_address = ('localhost', 12345) # Replace with your language server's address
tokens = get_semantic_tokens(file_path, language_server_address)
print("Semantic tokens:", tokens)

