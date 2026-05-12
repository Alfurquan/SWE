# Design in memory file system

## DESCRIPTION

Implement an in-memory file system that supports hierarchical directory structures with operations for creating directories (mkdir), listing contents (ls), creating/appending to files (addContentToFile), and reading file contents (readContentFromFile). The system must handle path parsing (e.g., /a/b/c), distinguish between files and directories, and return listings in lexicographical order. For example, calling mkdir("/a/b/c") should create nested directories, and addContentToFile("/a/b/file.txt", "hello") should create the file with content.

Input:
```
mkdir("/a/b/c")
addContentToFile("/a/b/file.txt", "hello")
ls("/a/b")
readContentFromFile("/a/b/file.txt")
```

Output:
```
["c", "file.txt"]
"hello"
```