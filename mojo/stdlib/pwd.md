# pwd

Provides access to the password database.

## Types

```mojo
@value
struct Passwd(Stringable):
    var pw_name: String    # User name
    var pw_passwd: String  # User password
    var pw_uid: Int        # User ID
    var pw_gid: Int        # Group ID
    var pw_gecos: String   # User information
    var pw_dir: String     # Home directory
    var pw_shell: String   # Shell program
```

## Functions

```mojo
# Retrieve password database entry by user name
fn getpwnam(name: String) raises -> Passwd

# Retrieve password database entry by user ID
fn getpwuid(uid: Int) raises -> Passwd
```