# python

Provides Python interoperability.

## Types

```mojo
@register_passable
struct PythonObject(ImplicitlyBoolable, ImplicitlyIntable, Indexer, KeyElement, SizedRaising, Stringable, Writable, _HashableWithHasher):
    # Methods
    fn __init__(out self)  # Initialize with None
    fn __init__(out self, ptr: PyObjectPtr)
    fn __init__(out self, none: NoneType)
    fn __init__(out self, value: Bool)
    fn __init__(out self, integer: Int)
    fn __init__[dt: DType](mut self, value: SIMD[dt, 1])
    fn __init__(out self, value: StringLiteral)
    fn __init__(out self, value: String)
    fn __init__(out self, string: StringSlice)
    fn __init__[*Ts: CollectionElement](mut self, value: ListLiteral[*Ts])
    fn __init__[*Ts: CollectionElement](mut self, value: Tuple[*Ts])
    fn __init__(out self, slice: Slice)
    fn __init__(out self, value: Dict[Self, Self])

    # Conversion methods
    fn __bool__(self) -> Bool
    fn __int__(self) -> Int
    fn __float__(self) -> Float64
    fn __str__(self) -> String

    # Python operations
    fn __getattr__(self, name: StringLiteral) raises -> PythonObject
    fn __setattr__(self, name: StringLiteral, new_value: PythonObject) raises
    fn __getitem__(self, *args: PythonObject) raises -> PythonObject
    fn __getitem__(self, *args: Slice) raises -> PythonObject
    fn __setitem__(mut self, *args: PythonObject, value: PythonObject) raises
    fn __call__(self, *args: PythonObject, **kwargs: PythonObject) raises -> PythonObject
    fn __iter__(self) raises -> _PyIter
    fn __contains__(self, rhs: PythonObject) raises -> Bool

    # Arithmetic operations
    fn __add__(self, rhs: PythonObject) raises -> PythonObject
    fn __sub__(self, rhs: PythonObject) raises -> PythonObject
    fn __mul__(self, rhs: PythonObject) raises -> PythonObject
    fn __truediv__(self, rhs: PythonObject) raises -> PythonObject
    fn __floordiv__(self, rhs: PythonObject) raises -> PythonObject
    fn __mod__(self, rhs: PythonObject) raises -> PythonObject
    fn __pow__(self, exp: PythonObject) raises -> PythonObject

@register_passable
struct TypedPythonObject[type_hint: StringLiteral](SizedRaising):
    var _obj: PythonObject

    # Specialized methods for different type hints
    fn __getitem__(self: TypedPythonObject["Tuple"], pos: I) raises -> PythonObject
```

## Functions

```mojo
struct Python:
    # Evaluation functions
    fn eval(mut self, code: StringSlice) -> Bool
    @staticmethod
    fn evaluate(expr: StringSlice, file: Bool = False, name: StringSlice[StaticConstantOrigin] = "__main__") raises -> PythonObject

    # Path functions
    @staticmethod
    fn add_to_path(dir_path: StringSlice) raises

    # Module operations
    @staticmethod
    fn import_module(module: StringSlice) raises -> PythonObject
    @staticmethod
    fn create_module(name: String) raises -> TypedPythonObject["Module"]
    @staticmethod
    fn add_functions(mut module: TypedPythonObject["Module"], owned functions: List[PyMethodDef]) raises
    @staticmethod
    fn add_object(mut module: TypedPythonObject["Module"], name: StringLiteral, value: PythonObject) raises

    # Container creation
    @staticmethod
    fn dict() -> PythonObject
    @staticmethod
    fn list() -> PythonObject

    # Utility methods
    @staticmethod
    fn none() -> PythonObject
    @staticmethod
    fn is_type(x: PythonObject, y: PythonObject) -> Bool
    @staticmethod
    fn type(obj: PythonObject) -> PythonObject
```