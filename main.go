package main

import (
    "embed"
    "fmt"
    "io/ioutil"
    "os"
    "os/exec"
)

//go:embed payload.py
var payload embed.FS

func main() {
    tmpFile, err := ioutil.TempFile("", "9k-*.py")
    if err != nil {
        fmt.Println("Failed to create temp file:", err)
        return
    }
    defer os.Remove(tmpFile.Name())

    pyCode, _ := payload.ReadFile("payload.py")
    tmpFile.Write(pyCode)
    tmpFile.Close()

    cmd := exec.Command("python3", tmpFile.Name())
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr
    cmd.Stdin = os.Stdin

    err = cmd.Run()
    if err != nil {
        fmt.Println("Execution failed:", err)
    }
}
