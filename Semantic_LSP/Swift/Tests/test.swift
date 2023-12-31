// Create and configure the sub-process
self.serverProcess = Process()
serverProcess.executableURL = URL(filePath: "/Library/Developer/CommandLineTools/usr/bin/sourcekit-lsp", directoryHint: .notDirectory)
serverProcess.arguments = ["--log-level", "debug"]
serverProcess.qualityOfService = .userInteractive
// Set current-working-directory to the directory of the codebase I want to browse
// I'm not sure if this is necessary, but likely doesn't hurt.
serverProcess.currentDirectoryURL = URL(fileURLWithPath: "/Users/feifan/Developer/tanagram/src/Visualize")

// Get access to stdin, stdout, and stderr
self.stdinPipe = Pipe()
serverProcess.standardInput = stdinPipe
self.stdoutPipe = Pipe()
serverProcess.standardOutput = stdoutPipe
stdoutPipe.fileHandleForReading.waitForDataInBackgroundAndNotify()
NotificationCenter.default.addObserver(
    forName: NSNotification.Name.NSFileHandleDataAvailable,
    object: stdoutPipe.fileHandleForReading,
    queue: nil,
    using: self.handleStdoutOutput(fromNotification:)
)
self.stderrPipe = Pipe()
serverProcess.standardError = stderrPipe
stderrPipe.fileHandleForReading.waitForDataInBackgroundAndNotify()
NotificationCenter.default.addObserver(
    forName: NSNotification.Name.NSFileHandleDataAvailable,
    object: stderrPipe.fileHandleForReading,
    queue: nil,
    using: self.handleStderrOutput(fromNotification:)
)

// Actually start the sub-process
try! serverProcess.run()
print("Running with PID \(serverProcess.processIdentifier)")

private func handleStdoutOutput(fromNotification notification: Notification) {
    guard let handle = notification.object as? FileHandle else { return }
    let data = handle.availableData
    if data.count > 0 {
        if let str = String(data: data, encoding: .utf8) {
            print("[SourceKit-LSP stdout] \(str)\n\n")
        } else {
            print("[SourceKit-LSP stdout] Got data, but couldn't convert it into a string\n\n")
        }
    } else {
        print("[SourceKit-LSP stdout] Reached end of input\n\n")
    }
    // In my testing, waitForDataInBackgroundAndNotify fires once (the next time there's data),
    // and not again. So in the notification handler, I call it again
    // to, effectively, loop the listener.
    self.stdoutPipe.fileHandleForReading.waitForDataInBackgroundAndNotify()
}