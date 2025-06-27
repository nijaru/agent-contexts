# Lightbug API Technical Documentation

## Metadata Section
```
TITLE: Lightbug API
VERSION: 0.1.0.dev2024092905
DOCUMENTATION_SOURCE: https://github.com/saviorand/lightbug_api
MODEL: Claude-3.7-Sonnet
```

## Conceptual Overview

- Lightbug API is a framework built on top of Lightbug HTTP that enables developers to quickly create expressive REST APIs in pure Mojo
- Features a simple and intuitive routing system for handling HTTP methods like GET, POST, PUT, and DELETE
- Designed for high performance while maintaining the ease of use familiar to Python web developers
- Leverages Mojo's static typing and optimization capabilities for better performance than typical Python frameworks
- Currently in development stage and not production-ready, but usable for experimentation and prototyping

## Technical Reference

### Core Components

#### App [`EXPERIMENTAL`]

**Package:** `lightbug_api`
**Available Since:** `v0.1.0.dev2024092905`
**Status:** Experimental

**Signature:**
```mojo
struct App:
    fn __init__(inout self)
    
    fn get(inout self, path: String, handler: fn(HTTPRequest) -> HTTPResponse) -> None
    fn post(inout self, path: String, handler: fn(HTTPRequest) -> HTTPResponse) -> None
    fn put(inout self, path: String, handler: fn(HTTPRequest) -> HTTPResponse) -> None
    fn delete(inout self, path: String, handler: fn(HTTPRequest) -> HTTPResponse) -> None
    
    fn start_server(self, address: String = "0.0.0.0:8080") raises -> None
```

**Dependencies/Imports:**
```mojo
from lightbug_api import App
from lightbug_http import HTTPRequest, HTTPResponse, OK, NotFound
```

**Usage Example:**
```mojo
from lightbug_api import App
from lightbug_http import HTTPRequest, HTTPResponse, OK

@always_inline
fn hello(req: HTTPRequest) -> HTTPResponse:
    return OK("Hello 🔥!")

@always_inline
fn printer(req: HTTPRequest) -> HTTPResponse:
    print("Got a request on ", req.uri.path, " with method ", req.method)
    return OK(req.body_raw)

fn main() raises:
    var app = App()
    app.get("/", hello)
    app.post("/", printer)
    app.start_server()  # Default is "0.0.0.0:8080"
```

**Context:**
- Purpose: Provides a clean API for defining routes and handling HTTP requests
- Patterns: Handler-based approach where functions are registered for specific routes and HTTP methods
- Alternatives: Using raw Lightbug HTTP requires manual route handling
- Limitations: Currently limited to basic routing without path parameters or query string parsing
- Related: Built on top of Lightbug HTTP for the underlying HTTP server implementation
- Behavior: Blocking on `start_server()` call which runs the HTTP server until interrupted

**Edge Cases and Anti-patterns:**
- Common Mistakes: Forgetting that handlers are always_inline functions which can lead to performance issues
- Anti-patterns:
```mojo
# ANTI-PATTERN (no always_inline):
fn slow_handler(req: HTTPRequest) -> HTTPResponse:
    # Performance will be worse without @always_inline
    return OK("Response")

# CORRECT:
@always_inline
fn fast_handler(req: HTTPRequest) -> HTTPResponse:
    return OK("Response")
```
- Edge Cases: Error handling is minimal in the current version, so exceptions in handlers may crash the server

### HTTPService Trait [`STABLE`]

**Package:** `lightbug_http.service`
**Status:** Stable

**Signature:**
```mojo
trait HTTPService:
    fn func(self, req: HTTPRequest) raises -> HTTPResponse:
        ...
```

**Dependencies/Imports:**
```mojo
from lightbug_http.service import HTTPService
```

**Usage Example:**
```mojo
from lightbug_http import *

@value
struct CustomHandler(HTTPService):
    fn func(self, req: HTTPRequest) raises -> HTTPResponse:
        # Process the request and return a response
        if req.uri.path == "/hello":
            return OK("Hello World!")
        else:
            return NotFound()
```

**Context:**
- Purpose: Defines the interface for HTTP request handlers
- Patterns: Implement this trait in custom structs to handle HTTP requests
- Alternatives: Using the App class for route-based handling
- Related: Lightbug HTTP primitives (HTTPRequest, HTTPResponse)

### Request and Response Types [`STABLE`]

**Package:** `lightbug_http`
**Status:** Stable

**Signature:**
```mojo
struct HTTPRequest:
    var uri: URI
    var method: String
    var headers: Headers
    var body_raw: DynamicVector[UInt8]
    
    fn __init__(inout self, uri: URI, headers: Headers, method: String = "GET")
    fn body_raw(self) -> DynamicVector[UInt8]

struct HTTPResponse:
    var status_code: Int
    var headers: Headers
    var body_raw: DynamicVector[UInt8]
    
    fn __init__(inout self, status_code: Int, headers: Headers, body: DynamicVector[UInt8])
```

**Utility Response Functions:**
```mojo
fn OK(body: DynamicVector[UInt8] | String) -> HTTPResponse
fn NotFound() -> HTTPResponse
```

**Dependencies/Imports:**
```mojo
from lightbug_http import HTTPRequest, HTTPResponse, OK, NotFound
```

**Usage Example:**
```mojo
from lightbug_http import HTTPRequest, HTTPResponse, OK, NotFound

@always_inline
fn handle_request(req: HTTPRequest) -> HTTPResponse:
    if req.uri.path == "/api/data":
        return OK("Here's your data!")
    else:
        return NotFound()
```

**Context:**
- Purpose: Core HTTP primitives for handling request data and creating responses
- Patterns: Use HTTPRequest to access incoming request details and create HTTPResponses for your API
- Related: URI and Headers structs for working with HTTP components

## Installation and Setup

### Prerequisites

- Mojo programming language (latest version)
- Git for cloning repositories

### Installation

1. Add the mojo-community channel to your mojoproject.toml:
```toml
[project]
channels = [
    "conda-forge", 
    "https://conda.modular.com/max", 
    "https://repo.prefix.dev/mojo-community"
]
```

2. Add lightbug_api and lightbug_http in dependencies:
```toml
[dependencies]
lightbug_api = ">=0.1.0.dev2024092905"
lightbug_http = ">=0.1.4"
```

3. Run the Mojo installation command:
```
magic install
```

## Creating a Basic API

Here's a step-by-step guide to create a simple API with Lightbug API:

1. Create a new .mojo file for your application
2. Import the necessary components
3. Define your handler functions
4. Set up the App and register routes
5. Start the server

Example implementation:

```mojo
from lightbug_api import App
from lightbug_http import HTTPRequest, HTTPResponse, OK

@always_inline
fn index(req: HTTPRequest) -> HTTPResponse:
    return OK("Welcome to my API!")

@always_inline
fn get_users(req: HTTPRequest) -> HTTPResponse:
    # In a real application, you would fetch users from a database
    return OK('["user1", "user2", "user3"]')

@always_inline
fn create_user(req: HTTPRequest) -> HTTPResponse:
    # In a real application, you would create a user in a database
    print("Creating user from data: ", String(req.body_raw))
    return OK("User created successfully")

fn main() raises:
    var app = App()
    
    # Register routes
    app.get("/", index)
    app.get("/users", get_users)
    app.post("/users", create_user)
    
    # Start the server
    print("API server starting on port 8080...")
    app.start_server()
```

## Roadmap and Future Features

Lightbug API is still in early development. Future planned features include:

- OpenAPI specification support for automatic API documentation
- Path parameters and query string parsing
- Middleware support
- Authentication and authorization
- Request validation
- More sophisticated routing with pattern matching
- JSON serialization/deserialization utilities

## Limitations and Considerations

- Still in experimental stage, not recommended for production use
- Performance may vary as the Mojo ecosystem evolves
- Limited error handling - exceptions in handlers may crash the server
- Lacks features found in mature API frameworks like authentication, validation, etc.
- Documentation is minimal at this stage of development

## Community and Support

- GitHub repository: https://github.com/saviorand/lightbug_api
- Issues and feature requests can be submitted on GitHub
- The project welcomes contributions through pull requests

## Related Projects

- Lightbug HTTP: The underlying HTTP framework
- EmberJson: A JSON parsing library that can be used with Lightbug API (separate project)
- lightbug_web: Planned future framework for full-stack web applications in Mojo
