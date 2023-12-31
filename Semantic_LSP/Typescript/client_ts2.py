import json
import subprocess
import threading
import time
import os


# Start the language server
lsp_process = subprocess.Popen(
    [
        'tsserver', 
    ],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
    text=True
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

print("Waiting for language server to start...")
# Initialize the language server
init_message = json.dumps({
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "processId": None,
        "rootUri": None,
        "capabilities": {},
    }
})
lsp_process.stdin.write(f"Content-Length: {len(init_message)}\r\n\r\n{init_message}\n")
lsp_process.stdin.flush()
time.sleep(2)

print("Opening document...")
# Open the document
document_open_request = json.dumps({
    "jsonrpc": "2.0",
    "method": "textDocument/didOpen",
    "params": {
        "textDocument": {
            "uri": f"file://{os.getcwd()}/Typescript/Tests/test.ts",
            "languageId": "typescript",
            "version": 1,
            "text": open(f"{os.getcwd()}/Typescript/Tests/test.ts").read()
        }
    }
})
lsp_process.stdin.write(f"Content-Length: {len(document_open_request)}\r\n\r\n{document_open_request}\n")
lsp_process.stdin.flush()
time.sleep(5)

print("Requesting semantic tokens...")
# Request semantic tokens
semantic_tokens_request = json.dumps({
    "jsonrpc": "2.0",
    "id": 2,
    "method": "textDocument/semanticTokens/full",
    "params": {
        "textDocument": {
            "uri": f"file://{os.getcwd()}/Typescript/Tests/test.ts"
        }
    }
})
lsp_process.stdin.write(f"Content-Length: {len(semantic_tokens_request)}\r\n\r\n{semantic_tokens_request}\n")
lsp_process.stdin.flush()
time.sleep(20)

print("Closing document...")
# Close the document
document_close_request = json.dumps({
    "jsonrpc": "2.0",
    "method": "textDocument/didClose",
    "params": {
        "textDocument": {
            "uri": f"file://{os.getcwd()}/Typescript/Tests/test.ts"
        }
    }
})
lsp_process.stdin.write(f"Content-Length: {len(document_close_request)}\r\n\r\n{document_close_request}\n")
lsp_process.stdin.flush()
time.sleep(2)

lsp_process.terminate()
