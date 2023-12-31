import json
import os
import asyncio

async def lsp_client():
    host = '127.0.0.1'  # The host where typescript-language-server is running
    port = 12392         # The port where typescript-language-server is listening

    reader, writer = await asyncio.open_connection(host, port)

    # Function to send a JSON RPC message
    async def send_message(message):
        message_json = json.dumps(message).encode('utf-8')
        # Prepend message with Content-Length header required by LSP
        message_length = len(message_json)
        print(f"Content-Length: {message_length}\r\n\r\n".encode('utf-8') + message_json)
        #writer.write(f"Content-Length: {message_length}\r\n\r\n".encode('utf-8') + message_json)
        #await writer.drain()
    
    async def receive_message():
        while True:
            content_length = int((await reader.readline()).decode('utf-8').split(":")[1].strip())
            await reader.readline()  # Read the next two CRLF characters
            message_text = (await reader.readexactly(content_length)).decode('utf-8')
            message = json.loads(message_text)

            if 'method' in message and message['method'] == 'window/showMessage':
                print("Notification from server:", message['params']['message'])
            elif 'method' in message and message['method'] == 'window/logMessage':
                print("Log from server:", message['params']['message'])
            elif 'method' in message:
                print(message["method"])
            else:
                return message

    # Initialize the server
    init_msg = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "processId": 12345,
            "rootUri": f"file://{os.getcwd()}/Go/Tests/",
            "capabilities": {
                "textDocument": {
                    "semanticTokens": {
                        "tokenTypes": [
                            "namespace", "type", "class", "enum", "interface",
                            "struct", "typeParameter", "parameter", "variable",
                            "property", "enumMember", "event", "function", "method",
                            "macro", "keyword", "modifier", "comment", "string",
                            "number", "regexp", "operator"
                        ],
                        "tokenModifiers": [
                            "declaration", "definition", "readonly", "static",
                            "deprecated", "abstract", "async", "modification",
                            "documentation", "defaultLibrary"
                        ],
                        "formats": ["relative"],
                        "requests": {
                            "full": True
                        }
                    },
                    "initializationOptions": {
                        "semanticTokens": True
                    }
                }
            },
        },
    }
    await send_message(init_msg)
    #print(f"Initialization Response: {await receive_message()}")

    # Notify the server that we're initialized
    initialized_msg = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "initialized",
        "params": {},
    }
    await send_message(initialized_msg)
    #print(f"Initialized Response: {await receive_message()}")

    # Open a document
    open_doc_msg = {
        "jsonrpc": "2.0",
        "method": "textDocument/didOpen",
        "params": {
            "textDocument": {
                "uri": "file:///path/to/your/file.ts",
                "languageId": "typescript",
                "version": 1,
                "text": "package main\n\nfunc main() {\n\t// Your Go code here\n}"
            }
        }
    }
    #await send_message(open_doc_msg)
    print(f"Open Document Response: {await receive_message()}")

    # Request semantic tokens
    semantic_tokens_msg = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "textDocument/semanticTokens/full",
        "params": {
            "textDocument": {
                "uri": "file:///path/to/your/file.ts"
            }
        }
    }
    await send_message(semantic_tokens_msg)
    #print(f"Semantic Tokens Response: {await receive_message()}")

    # Close the document
    close_doc_msg = {
        "jsonrpc": "2.0",
        "method": "textDocument/didClose",
        "params": {
            "textDocument": {
                "uri": "file:///path/to/your/file.ts"
            }
        }
    }
    await send_message(close_doc_msg)
    #print(f"Close Document Response: {await receive_message()}")

    # Close the server
    shutdown_msg = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "shutdown",
    }
    await send_message(shutdown_msg)
    #print(f"Shutdown Response: {await receive_message()}")

    writer.close()
    await writer.wait_closed()

asyncio.run(lsp_client())
