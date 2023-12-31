import json
import subprocess
import time
import os
import sys


print("Start the language server")
lsp_process = subprocess.Popen(
    ["typescript-language-server", "--stdio"],
    stdin=subprocess.PIPE,
    stdout=sys.stdout,
    stderr=sys.stderr
)

def write_message(lsp_process, message):
    message_json = json.dumps(message).encode('utf-8')
    print("\n=============================\n")
    print("Sending:\n")
    print(f"Content-Length: {len(message_json)}\r\n\r\n".encode('utf-8') + message_json)
    print("\n=============================\n")
    lsp_process.stdin.write(f"Content-Length: {len(message_json)}\r\n\r\n".encode('utf-8') + message_json)
    lsp_process.stdin.flush()

init_message = {
    "jsonrpc": "2.0",
    "method": "initialize",
    "id": 1,
    "params": {
        "rootUri": f"file://{os.getcwd()}/Typescript/Tests/",
        "capabilities": {},
        "initializationOptions": {
            "semanticTokens": True
        }
    },
}
write_message(lsp_process, init_message)
time.sleep(5)

initialized_notification = {
    "jsonrpc": "2.0",
    "method": "initialized",
    "params": {}
}
write_message(lsp_process, initialized_notification)
time.sleep(5)

document_open_notification = {
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
}
write_message(lsp_process, document_open_notification)
time.sleep(10)

semantic_tokens_request = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "textDocument/semanticTokens/full",
    "params": {
        "textDocument": {
            "uri": f"file://{os.getcwd()}/Typescript/Tests/test.ts"
        }
    }
}
write_message(lsp_process, semantic_tokens_request)
time.sleep(10)

document_close_notification = {
    "jsonrpc": "2.0",
    "method": "textDocument/didClose",
    "params": {
        "textDocument": {
            "uri": f"file://{os.getcwd()}/Typescript/Tests/test.ts"
        }
    }
}
write_message(lsp_process, document_close_notification)
time.sleep(2)

lsp_process.terminate()
