import json
import subprocess
import threading
import time
import os
import sys

def write_message(lsp_process, message):
    message_json = json.dumps(message).encode('utf-8')
    print("Sending:\n")
    print(f"Content-Length: {len(message_json)}\r\n\r\n".encode('utf-8') + message_json)
    lsp_process.stdin.write(f"Content-Length: {len(message_json)}\r\n\r\n".encode('utf-8') + message_json)
    lsp_process.stdin.flush()

# Start the language server
lsp_process = subprocess.Popen(
    ['sourcekit-lsp'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=sys.stderr,
)

def read_lsp_output():
    while True:
        line = lsp_process.stdout.readline()
        if line.strip():
            print("Received:", line)

# Start a thread to read the language server's output
thread = threading.Thread(
    target=read_lsp_output, 
    daemon=True
)
thread.start()

# Initialize the language server
init_message = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "processId": None,
        "rootUri": f"file://{os.getcwd()}/Swift/Tests/",
        "capabilities": {},
    }
}
write_message(lsp_process=lsp_process, message=init_message)
time.sleep(2)

# Notify the server that we're initialized
inited_message = {
    "jsonrpc": "2.0",
    "method": "initialized",
    "params": {},
}
write_message(lsp_process=lsp_process, message=inited_message)
time.sleep(2)

# Open the document
document_open_request = {
    "jsonrpc": "2.0",
    "method": "textDocument/didOpen",
    "params": {
        "textDocument": {
            "uri": f"file://{os.getcwd()}/Swift/Tests/test.swift",
            "languageId": "swift",
            "version": 1,
            "text": open(f"{os.getcwd()}/Swift/Tests/test.swift").read()
        }
    }
}
write_message(lsp_process=lsp_process, message=document_open_request)
time.sleep(5)

# Request semantic tokens
semantic_tokens_request = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "textDocument/semanticTokens/full",
    "params": {
        "textDocument": {
            "uri": f"file://{os.getcwd()}/Swift/Tests/test.swift"
        }
    }
}
write_message(lsp_process=lsp_process, message=semantic_tokens_request)
time.sleep(10)

# Close the document
document_close_request = {
    "jsonrpc": "2.0",
    "method": "textDocument/didClose",
    "params": {
        "textDocument": {
            "uri": f"file://{os.getcwd()}/Swift/Tests/test.swift"
        }
    }
}
write_message(lsp_process=lsp_process, message=document_close_request)
time.sleep(2)

lsp_process.terminate()
