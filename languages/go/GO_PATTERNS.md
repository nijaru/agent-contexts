# Go Patterns

*Actionable patterns for Go development*

## Error Handling

### Always Check Errors
```go
// ❌ WRONG - Ignoring errors
result, _ := someFunction()

// ✅ CORRECT - Handle errors
result, err := someFunction()
if err != nil {
    return fmt.Errorf("failed to process: %w", err)
}
```

### Error Wrapping
```go
// Wrap errors with context
if err := operation(); err != nil {
    return fmt.Errorf("operation failed: %w", err)
}
```

## Concurrency Patterns

### Goroutine with WaitGroup
```go
var wg sync.WaitGroup
for _, item := range items {
    wg.Add(1)
    go func(i Item) {
        defer wg.Done()
        process(i)
    }(item)
}
wg.Wait()
```

### Channel Patterns
```go
// Producer-consumer
ch := make(chan Data, 100) // Buffered channel

// Producer
go func() {
    defer close(ch)
    for _, d := range data {
        ch <- d
    }
}()

// Consumer
for d := range ch {
    process(d)
}
```

## Interface Design

### Small Interfaces
```go
// ✅ GOOD - Small, focused interface
type Reader interface {
    Read([]byte) (int, error)
}

// ❌ BAD - Large interface
type FileHandler interface {
    Read([]byte) (int, error)
    Write([]byte) (int, error)
    Close() error
    Seek(int64, int) (int64, error)
    // ... many more methods
}
```

## Testing Patterns

### Table-Driven Tests
```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name string
        a, b int
        want int
    }{
        {"positive", 2, 3, 5},
        {"negative", -1, -1, -2},
        {"zero", 0, 0, 0},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := Add(tt.a, tt.b); got != tt.want {
                t.Errorf("Add(%d, %d) = %d, want %d", 
                    tt.a, tt.b, got, tt.want)
            }
        })
    }
}
```

## Performance Tips

### Pre-allocate Slices
```go
// ❌ SLOWER - Growing slice
var results []Item
for _, x := range input {
    results = append(results, process(x))
}

// ✅ FASTER - Pre-allocated
results := make([]Item, 0, len(input))
for _, x := range input {
    results = append(results, process(x))
}
```

### Use strings.Builder
```go
// ❌ SLOWER - String concatenation
var s string
for _, part := range parts {
    s += part
}

// ✅ FASTER - strings.Builder
var b strings.Builder
for _, part := range parts {
    b.WriteString(part)
}
s := b.String()
```

## Common Commands
```bash
# Format code
go fmt ./...

# Run tests
go test ./...

# Run tests with coverage
go test -cover ./...

# Build
go build -o app ./cmd/main

# Install dependencies
go mod tidy
```