# stat

Provides file status constants and functions.

## Constants

```mojo
alias S_IFMT = 0o0170000    # Bit mask for file type
alias S_IFDIR = 0o040000    # Directory
alias S_IFCHR = 0o020000    # Character device
alias S_IFBLK = 0o060000    # Block device
alias S_IFREG = 0o0100000   # Regular file
alias S_IFIFO = 0o010000    # FIFO
alias S_IFLNK = 0o0120000   # Symbolic link
alias S_IFSOCK = 0o0140000  # Socket
```

## Functions

```mojo
# Check file type from mode
fn S_ISLNK[intable: Intable](mode: intable) -> Bool  # Is a symbolic link
fn S_ISREG[intable: Intable](mode: intable) -> Bool  # Is a regular file
fn S_ISDIR[intable: Intable](mode: intable) -> Bool  # Is a directory
fn S_ISCHR[intable: Intable](mode: intable) -> Bool  # Is a character device
fn S_ISBLK[intable: Intable](mode: intable) -> Bool  # Is a block device
fn S_ISFIFO[intable: Intable](mode: intable) -> Bool  # Is a FIFO
fn S_ISSOCK[intable: Intable](mode: intable) -> Bool  # Is a socket
```