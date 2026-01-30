# Aurecon.CoDe Library System Prompt

## Overview

The Aurecon.CoDe library ecosystem consists of four core libraries providing geometry processing, mathematical operations, and serialization capabilities. This system prompt documents all public APIs available for consuming systems.

## Library Structure

-   **Aurecon.CoDe.Base**: Core computer science objects and utilities
-   **Aurecon.CoDe.Mathematics**: Mathematical operations and data structures
-   **Aurecon.CoDe.Geometry**: Geometry kernel with primitive and complex geometric operations
-   **Aurecon.CoDe.Geometry.Serialization.Json**: JSON serialization for geometry objects

## Aurecon.CoDe.Base Library

### Primitive Type Operators

#### Point2D Operators

-   **Implicit Conversions**: `(double, double)`, `(int, int)` tuples
-   **Explicit Conversions**: `Point3D`, `Vector2D`, `Vector3D`, `double[]`, `Matrix`
-   **Arithmetic**: `==`, `!=`, `+`, `-` (unary/binary), `*`, `/`
-   **Mixed Operations**: Point + Vector, Point - Vector

#### Point3D Operators

-   **Implicit Conversions**: `(double, double, double)`, `(int, int, int)` tuples
-   **Explicit Conversions**: `Point2D`, `Vector2D`, `Vector3D`, `double[]`, Matrix
-   **Arithmetic**: `==`, `!=`, `+`, `-` (unary/binary), `*`, `/`
-   **Matrix Operations**: `Matrix * Point3D` for transformations

#### Point4D Operators (NURBS/Homogeneous Coordinates)

-   **Implicit Conversions**: `(double, double, double, double)`, `(double, double, double)`, `(int, int, int, int)`, `(int, int, int)` tuples
-   **Explicit Conversions**: All other point/vector types with perspective division, `double[]`, `Matrix`
-   **Arithmetic**: `+`, `-` (unary/binary), `*`, `/`

#### Vector2D Operators

-   **Implicit Conversions**: `(double, double)`, `(int, int)` tuples
-   **Explicit Conversions**: `Vector3D`, `Point2D`, `Point3D`, `double[]`, `Matrix`
-   **Arithmetic**: `==`, `!=`, `+`, `-` (unary/binary), `*`, `/`
-   **Mixed Operations**: Vector + Point, Vector - Point

#### Vector3D Operators

-   **Implicit Conversions**: `(double, double, double)`, `(int, int, int)` tuples
-   **Explicit Conversions**: `Point2D`, `Point3D`, `Vector2D`, `double[]`, `Matrix`
-   **Arithmetic**: `==`, `!=`, `+`, `-` (unary/binary), `*`, `/`
-   **Mixed Operations**: Vector + Point, Vector - Point

### Geometric Type Operators

#### Line Conversion Operators

-   **Explicit Conversions**: `LineSegment ↔ Line`, `Ray ↔ Line`

#### Transform Matrix Operators

-   **Comparison**: `==`, `!=`
-   **Matrix Operations**: `Transform * Transform`
-   **Geometric Transformations**: `Transform * Point2D/Point3D/Vector2D/Vector3D`

### Key Usage Patterns

-   **Tuple Construction**: All primitives support convenient tuple-based creation
-   **Mathematical Operations**: Standard arithmetic with proper type safety
-   **Type Conversions**: Explicit conversions for potentially lossy operations
-   **Matrix Integration**: Full support for matrix transformations
-   **Mixed Arithmetic**: Natural operations between points and vectors

### Design Principles

-   **Type Safety**: Implicit (safe) vs explicit (potentially lossy) conversions
-   **Mathematical Consistency**: Standard mathematical operator precedence
-   **Convenience**: Tuple-based construction reduces verbosity
-   **Performance**: Efficient implementations with minimal overhead
-   **Interoperability**: Full matrix operation support

### Core Classes and Interfaces

#### BaseObject Class

The fundamental building block of the library ecosystem. Provides dynamic property access and type conversion capabilities.

**Key Features:**

-   **Dynamic Properties**: Access and set properties using string keys via indexer `object this[string key]`
-   **Type Conversion**: Automatic conversion between different types using TypeMap
-   **Hierarchical Structure**: Support for nested objects and collections
-   **Unique Identification**: Each object has an auto-generated Id property

**Public API:**

```csharp
public class BaseObject : DynamicObject, IDynamicMetaObjectProvider, INotifyPropertyChanged
{
    public string Id { get; set; }
    public object this[string key] { get; set; }
    public IEnumerable<T> GetChildren<T>()
    public BaseObject()
    public BaseObject(object item)
    public virtual void SetProperties(IDictionary source)
}
```

**Usage Examples:**

-   Dynamic object creation: `var obj = new BaseObject(); obj["PropertyName"] = value;`
-   Type conversion: `var convertedObj = (TargetType)baseObject;`
-   Child extraction: `var childGeometries = baseObject.GetChildren<Point3D>();`

#### IDuplicatable<T> Interface

Ensures deep cloning capabilities for immutable contexts.

```csharp
public interface IDuplicatable<out T>
{
    T Duplicate();
}
```

**Purpose**: Use when objects need to be copied without affecting the original instance.

#### IValidatable Interface

Provides validation capabilities for objects that can be in invalid states.

```csharp
public interface IValidatable
{
    bool IsValid { get; }
}
```

**Purpose**: Use to check if geometry objects or mathematical constructs are valid before operations.

#### Optional<T> Struct

Type-safe nullable-like functionality for handling operations that may not have results.

**Key Features:**

-   **Safe Value Access**: `TryGetValue(out T value)` method
-   **Value Checking**: `HasValue` property
-   **Fluid API**: Extension methods `Some()` and `None()`

**Public API:**

```csharp
public readonly struct Optional<T>
{
    public bool HasValue { get; }
    public T Value { get; }
    public bool TryGetValue(out T value)
}

public static class Optional
{
    public static Optional<T> Some<T>(this T value)
    public static Optional<T> None<T>()
}
```

**Usage Examples:**

-   Creating optionals: `var result = value.Some();` or `var empty = Optional.None<string>();`
-   Safe access: `if (optional.TryGetValue(out var value)) { /* use value */ }`

#### TypeMap Class

Sophisticated type conversion system for dynamic object mapping.

**Key Features:**

-   **Dynamic Registration**: Register custom type converters
-   **Automatic Conversion**: Convert between registered types
-   **Singleton Pattern**: Global instance accessible via `TypeMap.Instance`

**Public API:**

```csharp
public class TypeMap
{
    public static readonly TypeMap Instance;
    public Optional<TTo> Convert<TTo>(dynamic input, Action<Exception> onException = null)
    public Optional<dynamic> Convert(dynamic input, Type targetType, Action<Exception> onException = null)
    public TypeMap Duplicate()
}
```

**Usage Examples:**

-   Type conversion: `var result = TypeMap.Instance.Convert<TargetType>(sourceObject);`
-   Custom mappings: Register converters for specific type pairs

### Collection Extensions

#### IEnumerable Extensions

Extension methods for enhanced LINQ operations.

**Public API:**

```csharp
public static class IEnumerableT
{
    public static IEnumerable<TResult> Permute<TSource, TOtherSource, TResult>(
        this IEnumerable<TSource> source,
        IEnumerable<TOtherSource> otherSource,
        Func<TSource, TOtherSource, TResult> typeMap)

    public static IEnumerable<Tuple<T, T>> Pairwise<T>(this IEnumerable<T> source)

    public static IEnumerable<T> Difference<T>(this IEnumerable<T> source, IEnumerable<T> other)

    public static IEnumerable<T> Return<T>(T item)
}
```

**Usage Examples:**

-   Permutations: `list1.Permute(list2, (a, b) => new { A = a, B = b })`
-   Pairwise processing: `points.Pairwise().Select(pair => CalculateDistance(pair.Item1, pair.Item2))`
-   Set differences: `collection1.Difference(collection2)`

### Storage System

#### IStore Interface

Base interface for property storage mechanisms.

```csharp
public interface IStore
{
    bool TryGetProperty(string key, out object value);
    bool SetProperty(string key, object value);
    IEnumerable<string> GetPropertyKeys();
    IEnumerable<KeyValuePair<string, object>> GetChildren();
    IEnumerable<KeyValuePair<string, T>> GetChildren<T>();
}
```

**Purpose**: Abstraction layer for different storage backends (reflection, dictionary, etc.)

**Storage Implementations:**

-   **DictionaryStore**: Dictionary-based property storage
-   **ReflectionStore**: Reflection-based property access for objects
-   **StoreCollection**: Composite store that manages multiple IStore instances

## Aurecon.CoDe.Geometry Library

### Core Interfaces and Classes

#### IGeometry Interface

The fundamental interface that all geometry objects implement. Combines multiple behavioral interfaces:

```csharp
public interface IGeometry : IValidatable, ITransformable, IBoundable, IDuplicatable<IGeometry>
{
}
```

**Key Features:**

-   **Validation**: All geometry objects can validate their state
-   **Transformation**: Support for geometric transformations
-   **Bounding**: Ability to calculate bounding boxes
-   **Duplication**: Deep cloning capabilities

#### GeometryObject Class

A dynamic geometry container that extends BaseObject with geometry-specific functionality.

**Key Features:**

-   **Dynamic Properties**: Store any geometry objects as properties
-   **Bounding Box Calculation**: Automatically calculates union of all child bounding boxes
-   **Validation**: Aggregates validation from all contained geometries
-   **Type Conversion**: Automatic conversion to specific geometry types

**Public API:**

```csharp
public class GeometryObject : BaseObject, IGeometry
{
    public virtual BoundingBox GetBoundingBox()
    public virtual bool IsValid { get; }
    public virtual bool Transform(Transform transform)
    public virtual IGeometry Duplicate()
}
```

**Usage Examples:**

-   Dynamic creation: `var obj = new GeometryObject(); obj["Line"] = new LineSegment(pt1, pt2);`
-   Type conversion: `Point3D point = (Point3D)geometryObject;`

---

## Aurecon.CoDe.Geometry.Serialization.Json Library

The Serialization.Json library provides comprehensive JSON serialization and deserialization capabilities for all geometry objects in the ecosystem. It includes optimized converters, extension methods, and a unified serialization framework.

### Core Classes

#### `GeometrySerializer`

The main serialization class with pre-configured converters and modifiers for geometry objects.

**Constructor:**

```csharp
public GeometrySerializer()
```

**Properties:**

```csharp
public JsonSerializerOptions Options { get; set; }
public static string GeometryTypePropertyName { get; }
public static Dictionary<string, Type> GeometryTypes { get; }
```

**Serialization Methods:**

```csharp
public string Serialize<T>(T obj)
public void Serialize(Utf8JsonWriter writer, object obj)
```

**Deserialization Methods:**

```csharp
public T Deserialize<T>(string json)
public T Deserialize<T>(JsonElement element)
public object Deserialize(string json, Type returnType)
public object Deserialize(JsonElement element, Type returnType)
public T Deserialize<T>(ref Utf8JsonReader reader)
```

**Usage Example:**

```csharp
var serializer = new GeometrySerializer();

// Serialize a point
var point = new Point3D(1, 2, 3);
string json = serializer.Serialize(point);

// Deserialize back to object
var deserializedPoint = serializer.Deserialize<Point3D>(json);
```

### Extension Methods

The library provides extensive extension methods for direct serialization of geometry objects.

#### Serialization Extensions (`SerializationExtensions`)

**Mathematical Objects:**

```csharp
public static string Serialize(this Domain domain)
public static void Serialize(this Domain domain, Utf8JsonWriter writer)
```

**Primitive Objects:**

```csharp
public static string Serialize(this Plane plane)
public static string Serialize(this Point2D point2D)
public static string Serialize(this Point3D point3D)
public static string Serialize(this Point4D point4D)
public static string Serialize(this Ray ray)
public static string Serialize(this Vector2D vector2D)
public static string Serialize(this Vector3D vector3D)
```

**Curve Objects:**

```csharp
public static string Serialize(this Arc arc)
public static string Serialize(this Circle circle)
public static string Serialize(this Clothoid clothoid)
public static string Serialize(this Ellipse ellipse)
public static string Serialize(this LineSegment line)
public static string Serialize(this NurbsCurve nurbsCurve)
public static string Serialize(this Parabola parabola)
public static string Serialize(this Polycurve polycurve)
public static string Serialize(this Polyline polyline)
```

**Shape Objects:**

```csharp
public static string Serialize(this IShape2D shape)
public static string Serialize(this Disc disc2D)
public static string Serialize(this Rectangle rectangle)
public static string Serialize(this RoundedRectangle roundedRectangle)
public static string Serialize(this GenericShape shape)
```

**Mesh Objects:**

```csharp
public static string Serialize(this MeshFace meshFace)
public static string Serialize(this TriMesh triMesh)
public static string Serialize(this FVMesh fvMesh)
```

**Solid Objects:**

```csharp
public static string Serialize(this Extrusion extrusion)
public static string Serialize(this Loft loft)
public static string Serialize(this Sweep sweep)
```

**Spatial Objects:**

```csharp
public static string Serialize(this BoundingBox boundingBox)
public static string Serialize(this Box box)
public static string Serialize(this NurbsSurface nurbsSurface)
public static string Serialize(this Rectangle3D rectangle)
public static string Serialize(this Triangle3D triangle)
```

**Usage Example:**

```csharp
// Direct serialization using extension methods
var line = new LineSegment(new Point3D(0, 0, 0), new Point3D(1, 1, 1));
string json = line.Serialize();

// Serialization to writer
using var stream = new MemoryStream();
using var writer = new Utf8JsonWriter(stream);
line.Serialize(writer);
```

#### Deserialization Extensions

**String Extensions (`StringExtensions`):**

```csharp
public static T Deserialize<T>(this string json)
```

**JsonElement Extensions (`JsonElementExtensions`):**

```csharp
public static T Deserialize<T>(this JsonElement jsonElement)
```

**Usage Example:**

```csharp
// Deserialize from JSON string
string json = @"{""start"":{""x"":0,""y"":0,""z"":0},""end"":{""x"":1,""y"":1,""z"":1}}";
var line = json.Deserialize<LineSegment>();

// Deserialize from JsonElement
JsonDocument doc = JsonDocument.Parse(json);
var lineFromElement = doc.RootElement.Deserialize<LineSegment>();
```

### JsonSerializerOptions Extensions

The library provides utilities for manipulating JsonSerializerOptions for custom serialization scenarios.

#### `JsonSerializerOptionsExtensions`

**Methods:**

```csharp
public static JsonSerializerOptions Duplicate(this JsonSerializerOptions options, List<Type> convertersToExclude = null)
public static JsonSerializerOptions Duplicate(this JsonSerializerOptions options, Type converterToRemove)
public static void RemoveConverter(this JsonSerializerOptions options, Type converterType)
public static void RemoveConverter<T>(this JsonSerializerOptions options) where T : JsonConverter
```

**Usage Example:**

```csharp
var originalOptions = new GeometrySerializer().Options;
var customOptions = originalOptions.Duplicate(typeof(LineSegmentConverter));
```

### Specialized Converters

The library includes optimized JSON converters for complex geometry types:

-   `BaseObjectConverter` and `BaseObjectConverterFactory` - Handles BaseObject-derived types
-   `GeometryObjectConverter` - Specialized converter for geometry objects
-   `InterfaceConverter<T>` - Handles interface-based serialization (IGeometry, ICurve, IShape)
-   Specific converters for complex types: `ExtrusionConverter`, `LoftConverter`, `SweepConverter`, `FVMeshConverter`, etc.

### Key Features

1. **Comprehensive Coverage**: Supports all geometry types in the ecosystem
2. **Performance Optimized**: Specialized converters for complex types
3. **Flexible API**: Multiple serialization approaches (direct, writer-based, extension methods)
4. **Type Safety**: Strong typing with generic methods
5. **Custom Configuration**: Extensible options and modifier system
6. **Interface Support**: Handles polymorphic serialization of geometry interfaces

### Integration Example

```csharp
// Complete serialization workflow
using Aurecon.CoDe.Geometry.Serialization.Json;

// Create complex geometry
var points = new[] { new Point3D(0, 0, 0), new Point3D(1, 0, 0), new Point3D(1, 1, 0) };
var polyline = new Polyline(points);
var disc = new Disc(new Point3D(0.5, 0.5, 0), 0.3);

// Serialize individually
string polylineJson = polyline.Serialize();
string discJson = disc.Serialize();

// Serialize collection
var geometries = new IGeometry[] { polyline, disc };
var serializer = new GeometrySerializer();
string collectionJson = serializer.Serialize(geometries);

// Deserialize back
var deserializedPolyline = polylineJson.Deserialize<Polyline>();
var deserializedCollection = collectionJson.Deserialize<IGeometry[]>();
```

---

## Aurecon.CoDe.Mathematics Library

### Core Mathematical Types

#### Polynomial Struct

Represents polynomial functions with full mathematical operations.

**Public API:**

```csharp
public struct Polynomial : IFunctionXY
{
    public double[] Coefficients { get; }
    public int Degree { get; }
    public Domain Domain { get; set; }
    public double Length { get; }
    public bool IsValid { get; }

    // Constructors
    public Polynomial(double[] coefficients, Domain domain = default)
    public Polynomial(double linearCoefficient = 1, double constant = 0, Domain domain = default)
    public Polynomial(double quadraticCoefficient = 1, double linearCoefficient = 0, double constant = 0, Domain domain = default)
    public Polynomial(double cubicCoefficient = 1, double quadraticCoefficient = 0, double linearCoefficient = 0, double constant = 0, Domain domain = default)
    public Polynomial(double[] xs, double[] ys, Domain domain = default) // Interpolation constructor

    // Evaluation Methods
    public double GetValueAt(double x)
    public double GetFirstDerivativeAt(double x)
    public double GetSecondDerivativeAt(double x)
    public double GetCurvatureAt(double x)
    public double GetLengthAt(double x)
    public double GetValueAtLength(double length, double tolerance = Tolerance.ABSOLUTE_TOLERANCE)

    // Mathematical Operations
    public Polynomial GetDerivative(int n)
    public Polynomial GetIntegral(int n)
}
```

**Usage Examples:**

```csharp
// Create quadratic polynomial: f(x) = 2x² + 3x + 1
var poly = new Polynomial(2, 3, 1);
double value = poly.GetValueAt(2); // Evaluates to 15

// Find derivative
Polynomial derivative = poly.GetDerivative(1); // f'(x) = 4x + 3

// Interpolate through points
double[] xs = {1, 2, 3};
double[] ys = {2, 4, 8};
var interpolated = new Polynomial(xs, ys);
```

#### Matrix Struct

Matrix operations with linear algebra support.

**Public API:**

```csharp
public struct Matrix : IMatrix
{
    public int Rows { get; }
    public int Columns { get; }
    public double[] this[int row] { get; set; }
    public bool IsValid { get; }

    // Constructors
    public Matrix(int rows, int columns)
    public Matrix(double[,] values)

    // Matrix Operations
    public void Decompose(out IMatrix LU, out int[] P)
    public double[] LUSolve(int[] P, double[] b)
    public Matrix Transpose()
    public double Determinant()
    public Matrix Inverse()

    // Static Factory Methods
    public static Matrix Identity(int size)
    public static Matrix Zero(int rows, int columns)
}
```

#### Domain Struct

Represents mathematical intervals and ranges.

**Public API:**

```csharp
public struct Domain
{
    public double Start { get; set; }
    public double End { get; set; }
    public double Length { get; }
    public double Mid { get; }
    public bool IsValid { get; }

    // Constructors
    public Domain(double start, double end)

    // Domain Operations
    public bool Contains(double value)
    public bool Contains(Domain other)
    public bool Overlaps(Domain other)
    public Domain Union(Domain other)
    public Domain Intersection(Domain other)
    public double RemapParameter(double parameter, Domain targetDomain)
    public double Clamp(double value)
}
```

### Mathematical Extension Methods

#### Function Extensions

Extension methods for Func<double, double> providing advanced mathematical operations.

**Public API:**

```csharp
public static class Extensions
{
    // Integration
    public static double Integrate(this Func<double, double> function, Domain domain, int iterations = 20)

    // Root Finding
    public static double FindRoot(this Func<double, double> function,
                                 Func<double, double> functionDerivative,
                                 Func<double, bool> terminationCondition,
                                 double guess, Domain functionDomain, int iterations = 100)

    // Polynomial Extensions
    public static double[] FindRoots(this Polynomial polynomial)
    public static double[] FindTurningPoints(this Polynomial polynomial)
    public static double[] FindRoots(this Func<double, double> function, Domain domain)
    public static double[] FindTurningPoints(this Func<double, double> function, Domain domain)

    // Differentiation
    public static Func<double, double> GetDerivative(this Func<double, double> function, int order = 1)
}
```

**Usage Examples:**

```csharp
// Integration
Func<double, double> f = x => x * x;
double area = f.Integrate(new Domain(0, 1)); // ≈ 1/3

// Root finding
Func<double, double> g = x => x * x - 2;
Func<double, double> dg = x => 2 * x;
double root = g.FindRoot(dg, x => Math.Abs(g(x)) < 1e-8, 1, new Domain(0, 2)); // ≈ √2
```

#### Double Extensions

Utility extensions for double values.

**Public API:**

```csharp
public static class DoubleExtensionMethods
{
    // Angle Conversions
    public static double ToDegrees(this double angle)
    public static double ToRadians(this double angle)
    public static double ArcRadiansAngle(this double angle)

    // Validation and Clamping
    public static bool IsValid(this double value)
    public static double Clamp(this double value, double min, double max)
    public static double Clamp(this double value, Domain domain)
}
```

#### Integer Extensions

Mathematical operations for integers.

**Public API:**

```csharp
public static class IntegerExtensionMethods
{
    public static int Clamp(this int value, int min, int max)
    public static double Clamp(this int value, Domain domain)
    public static int[] Binomial(this int n)
    public static int Factorial(this int n)
    public static int Choose(this int numberOfTrials, int numberOfSuccesses)
}

public static class UnsignedIntegerExtensionMethods
{
    public static uint[] Binomial(this uint n)
    public static uint Factorial(this uint n)
    public static uint Choose(this uint numberOfTrials, uint numberOfSuccesses)
}
```

### Interpolation System

#### INumericalInterpolationMethod Interface

Base interface for interpolation algorithms.

**Public API:**

```csharp
public interface INumericalInterpolationMethod
{
    double Interpolate(double value);
}
```

#### Built-in Interpolation Methods

**Linear Interpolation:**

```csharp
public class Linear : INumericalInterpolationMethod
{
    public double Interpolate(double value) => value;
}
```

**Fade Interpolation:**

```csharp
public class Fade : INumericalInterpolationMethod
{
    public double Interpolate(double value) => 6*value⁵ - 15*value⁴ + 10*value³;
}
```

**Quadratic Easing:**

```csharp
public class QuadraticEaseIn : INumericalInterpolationMethod
{
    public double Interpolate(double value) => value * value;
}

public class QuadraticEaseOut : INumericalInterpolationMethod
{
    public double Interpolate(double value)
    {
        value = 1 - value;
        return 1 - value * value;
    }
}

public class QuadraticEaseInEaseOut : INumericalInterpolationMethod
{
    public double Interpolate(double value)
    {
        if (value < 0.5)
            return 2 * value * value;
        value = 1 - value;
        return 1 - 2 * value * value;
    }
}
```

**Sine Easing:**

```csharp
public class SineEaseIn : INumericalInterpolationMethod
{
    public double Interpolate(double value) => 1 - Math.Cos(0.5 * value * Math.PI);
}

public class SineEaseOut : INumericalInterpolationMethod
{
    public double Interpolate(double value) => Math.Sin(0.5 * value * Math.PI);
}

public class SineEaseInEaseOut : INumericalInterpolationMethod
{
    public double Interpolate(double value) => 0.5 - 0.5 * Math.Cos(Math.PI * value);
}
```

**Usage Examples:**

```csharp
// Using different interpolation methods
var linear = new Linear();
var easeIn = new QuadraticEaseIn();
var sineOut = new SineEaseOut();

double t = 0.5;
double linearValue = linear.Interpolate(t);     // 0.5
double easeInValue = easeIn.Interpolate(t);     // 0.25
double sineValue = sineOut.Interpolate(t);      // ≈ 0.707
```

### Graph Theory System

#### IGraph<V, E> Interface

Generic graph interface supporting various graph algorithms.

**Public API:**

```csharp
public interface IGraph<V, E> : IDuplicatable<IGraph<V, E>>
{
    // Graph Structure
    int VertexCount { get; }
    int EdgeCount { get; }
    V[] Vertices { get; }
    VertexTopology<V, E> this[V vertex] { get; }

    // Graph Modification
    bool AddVertex(V vertex)
    bool AddEdge(V from, E data, V to, double weight = 1.0)
    bool RemoveVertex(V vertex)
    bool RemoveEdge(V from, V to)

    // Graph Analysis
    V[] GetRoots()
    V[] GetLeaves()

    // Shortest Path Operations
    bool GetShortestPath(V from, V to, out V[] shortestPath, out double pathLength,
                        IShortestPathAlgorithm<V, E> algorithm = null)
    Dictionary<V, double> GetShortestPathsAt(V vertex)
    Dictionary<V, Dictionary<V, double>> GetAllShortestPaths()

    // Centrality Measures
    Dictionary<V, double> GetClosenessValues()
    Dictionary<V, double> GetBetweennessValues()
    Dictionary<V, int> GetDegreeInValues()
    Dictionary<V, int> GetDegreeOutValues()
}
```

#### Graph Implementations

**Graph<V, E> - Undirected Graph:**

```csharp
public class Graph<V, E> : IGraph<V, E>
{
    // Implements all IGraph<V, E> methods for undirected graphs
}
```

**DirectedGraph<V, E> - Directed Graph:**

```csharp
public class DirectedGraph<V, E> : IGraph<V, E>
{
    // Implements all IGraph<V, E> methods for directed graphs
}
```

**DirectedAcyclicGraph<V, E> - DAG:**

```csharp
public class DirectedAcyclicGraph<V, E> : IGraph<V, E>
{
    // Additional DAG-specific methods
    bool DownstreamContains(V startingVertex, V vertexToFind)
}
```

**Tree<V, E> - Tree Structure:**

```csharp
public class Tree<V, E> : IGraph<V, E>
{
    // Tree-specific optimizations and methods
    bool DownstreamContains(V startingVertex, V vertexToFind)
}
```

#### Shortest Path Algorithms

**IShortestPathAlgorithm<V, E> Interface:**

```csharp
public interface IShortestPathAlgorithm<V, E>
{
    bool Evaluate(V source, V target, out V[] shortestPath, out double pathLength)
    bool Evaluate(V source, V target, out V[] shortestVertexPath,
                 out EdgeTopology<V, E>[] shortestEdgePath, out double pathLength)
    bool Evaluate(V source, V target, out EdgeTopology<V, E>[] shortestPath, out double pathLength)
}
```

**Dijkstra's Algorithm:**

```csharp
public readonly struct Dijkstra<V, E> : IShortestPathAlgorithm<V, E>
{
    public Dijkstra(IGraph<V, E> graph)
    // Implements Dijkstra's shortest path algorithm
}
```

**A\* Algorithm:**

```csharp
public readonly struct AStar<V, E> : IShortestPathAlgorithm<V, E>
{
    public AStar(IGraph<V, E> graph, Func<V, V, double> heuristic)
    // Implements A* search algorithm with heuristic function
}
```

**Usage Examples:**

```csharp
// Create and populate graph
var graph = new DirectedGraph<string, object>();
graph.AddEdge("A", null, "B", 1);
graph.AddEdge("B", null, "C", 2);
graph.AddEdge("A", null, "C", 4);

// Find shortest path
bool found = graph.GetShortestPath("A", "C", out string[] path, out double length);
// found = true, path = ["A", "B", "C"], length = 3

// Use specific algorithm
var dijkstra = new Dijkstra<string, object>(graph);
found = dijkstra.Evaluate("A", "C", out path, out length);

// A* with heuristic
Func<string, string, double> heuristic = (from, to) => 0; // Simple heuristic
var aStar = new AStar<string, object>(graph, heuristic);
found = aStar.Evaluate("A", "C", out path, out length);
```

### Collection Extensions

#### DoubleEnumerable Extensions

Mathematical operations on collections of doubles.

**Public API:**

```csharp
public static class DoubleEnumerable
{
    // Statistical Methods
    public static double Variance(this IEnumerable<double> values, bool isEstimation)
    public static double StandardDeviation(this IEnumerable<double> values, bool isEstimation)

    // Regression Analysis
    public static double[] LeastSquares(this IEnumerable<IEnumerable<double>> data, bool isEstimation)
    public static double[] LeastSquares(this IEnumerable<IEnumerable<double>> data, out double variance, bool isEstimation)

    // Search Operations
    public static int BinarySearchSpan(this IEnumerable<double> sortedValues, double t, int beforeRange, int afterRange)
}
```

### Tolerance and Validation

#### Tolerance Class

Global tolerance settings for floating-point comparisons.

**Public API:**

```csharp
public static class Tolerance
{
    public const double ABSOLUTE_TOLERANCE = 1e-10;
    public const double RELATIVE_TOLERANCE = 1e-10;
    public const double ANGULAR_TOLERANCE = 1e-8;
}
```

### Primitive Geometry Types

#### Point3D Struct

Represents a point in 3D space with extensive geometric operations.

**Public API:**

```csharp
public struct Point3D : IPrimitive<Point3D>, IGeometry
{
    public double X { get; set; }
    public double Y { get; set; }
    public double Z { get; set; }

    // Constructors
    public Point3D(double x, double y, double z)

    // Key Methods
    public double DistanceTo(Point3D other)
    public double DistanceToSquared(Point3D other)
    public Vector3D To(Point3D other)
    public bool EqualsWithinTolerance(object obj, double tolerance)
    public bool Transform(Transform transform)
    public IGeometry Duplicate()
    public BoundingBox GetBoundingBox()
}
```

**Usage Examples:**

-   Creation: `var point = new Point3D(1.0, 2.0, 3.0);`
-   Distance calculation: `double dist = point1.DistanceTo(point2);`
-   Vector creation: `Vector3D vec = point1.To(point2);`

#### Vector3D Struct

Represents a vector in 3D space with comprehensive vector operations.

**Public API:**

```csharp
public struct Vector3D : IPrimitive<Vector3D>, IGeometry
{
    public double X { get; set; }
    public double Y { get; set; }
    public double Z { get; set; }
    public double Magnitude { get; }
    public double MagnitudeSquared { get; }

    // Constructors
    public Vector3D(double x, double y, double z)
    public Vector3D(Point3D from, Point3D to)

    // Vector Operations
    public Vector3D Cross(Vector3D other)
    public Vector3D Cross(Point3D other)
    public double Dot(Vector3D other)
    public double Dot(Point3D other)
    public double GetAngle(Vector3D other)
    public double GetAbsoluteAngleWith(Vector3D other, Plane plane)
    public Vector3D GetProjectionOnToVector(Vector3D other)
    public Vector3D GetRejectionOnToVector(Vector3D other)
    public Vector3D GetProjectionOnToPlane(Plane plane)
    public bool Unitise()
    public bool Rotate(double angle, Vector3D axis)
    public double[] ToArray()
}
```

**Usage Examples:**

-   Creation: `var vector = new Vector3D(1, 0, 0);`
-   Cross product: `Vector3D cross = vec1.Cross(vec2);`
-   Normalization: `vector.Unitise();`
-   Angle calculation: `double angle = vec1.GetAngle(vec2);`

#### Line Struct

Represents an infinite mathematical line with intersection and proximity capabilities.

**Public API:**

```csharp
public struct Line : IPrimitive<Line>, IGeometry
{
    public Point3D Origin { get; set; }
    public Vector3D Direction { get; set; }
    public bool IsValid { get; }
    public bool IsDeformable { get; }

    // Intersection API
    public LineIntersecter Intersection { get; }
    public LineCoincidence Coincidence { get; }
    public LineProximity Proximity { get; }

    // Constructors
    public Line(Point3D startPoint, Point3D endPoint)
    public Line(Point3D startPoint, Vector3D direction)
    public Line(Point3D startPoint, Vector3D direction, double length)

    // Key Methods
    public Point3D GetPointAt(double t)
    public double GetClosestParameter(Point3D point)
    public Point3D GetClosestPoint(Point3D point)
    public bool Contains(Point3D point, double tolerance)
}
```

**Usage Examples:**

-   Creation: `var line = new Line(new Point3D(0,0,0), new Vector3D(1,0,0));`
-   Point evaluation: `Point3D pt = line.GetPointAt(0.5);`
-   Intersection: `bool intersects = line.Intersection.With(otherLine);`

#### Plane Struct

Represents a plane in 3D space with orientation and transformation capabilities.

**Public API:**

```csharp
public struct Plane : IPrimitive<Plane>, IGeometry
{
    public Point3D Origin { get; set; }
    public Vector3D XAxis { get; set; }
    public Vector3D YAxis { get; set; }
    public Vector3D ZAxis { get; }
    public Vector3D Normal { get; }

    // Key Methods
    public Point3D GetPointAt(double u, double v, double w)
    public bool Align(Vector3D alignmentVector, int vectorToAlignTo)
    public bool Flip(bool flipX, bool flipY)
    public bool Translate(Vector3D translationVector)
    public bool Rotate(double angle)
    public bool Rotate(double angle, Vector3D axis)
}
```

### Curve Types

#### ICurve Interface

Base interface for all curve types providing common curve operations.

```csharp
public interface ICurve : IGeometry
{
    Domain Domain { get; set; }
    double Length { get; }
    bool IsClosed { get; }
    bool IsDeformable { get; }

    // Evaluation Methods
    Point3D GetPointAt(double t)
    Vector3D GetTangentAt(double t)
    Vector3D GetCurvatureAt(double t)
    double GetParameterAt(double length)

    // Curve Operations
    bool ReparameteriseByLength()
    bool Reverse()
    bool Split(double t, out ICurve left, out ICurve right)
    ICurve Trim(Domain domain)

    // Intersection API (accessed via curve.Intersection.With(...))
    // Proximity API (accessed via curve.Proximity.With(...))
    // Coincidence API (accessed via curve.Coincidence.With(...))
}
```

#### LineSegment Struct

A finite line segment between two points.

**Public API:**

```csharp
public struct LineSegment : ICurve
{
    public Point3D StartPoint { get; set; }
    public Point3D EndPoint { get; set; }
    public Vector3D Direction { get; }
    public double Length { get; }
    public Domain Domain { get; set; }

    // Intersection API
    public LineSegmentIntersecter Intersection { get; }
    public LineSegmentCoincidence Coincidence { get; }
    public LineSegmentProximity Proximity { get; }

    // Constructors
    public LineSegment(Point3D startPoint, Point3D endPoint)
    public LineSegment(Point3D startPoint, Vector3D direction)
    public LineSegment(Point3D startPoint, Vector3D direction, double length)
}
```

#### Circle Struct

Represents a circle in 3D space.

**Key Features:**

-   **Parametric Evaluation**: Get points along the circle
-   **Geometric Properties**: Radius, center, plane of circle
-   **Intersection Operations**: With other curves and shapes

#### Arc Struct

Represents a circular arc with start and end angles.

#### Ellipse Struct

Represents an ellipse in 3D space with major and minor axes.

#### Polyline Class

A connected sequence of line segments.

**Public API:**

```csharp
public class Polyline : ICurve, ICollection<Point3D>
{
    public Point3D this[int index] { get; set; }
    public int Count { get; }
    public bool IsClosed { get; set; }

    // Collection Operations
    public void Add(Point3D point)
    public bool Remove(Point3D point)
    public void Clear()
    public bool Contains(Point3D point)

    // Curve Operations
    public Point3D GetPointAt(double t)
    public Vector3D GetTangentAt(double t)
    // ... other ICurve methods
}
```

#### Polycurve Class

A sequence of connected curves of different types.

### Shape Types

#### IShape Interface

Base interface for 2D shapes that can be filled or have boundaries.

```csharp
public interface IShape : IGeometry
{
    double Area { get; }
    Point2D Centroid { get; }
    Plane Plane { get; }

    // Boundary Access
    ICurve GetBoundary()
    ICurve[] GetVoids()

    // Containment
    bool Contains(Point2D point)
    bool Contains(Point3D point)

    // Shape Operations
    IShape Union(IShape other)
    IShape Intersection(IShape other)
    IShape Difference(IShape other)
}
```

#### Rectangle Class

Represents a rectangular shape.

**Public API:**

```csharp
public class Rectangle : IShape
{
    public Point2D Origin { get; set; }
    public double Width { get; set; }
    public double Height { get; set; }
    public Plane Plane { get; set; }

    // Constructors
    public Rectangle(Point2D origin, double width, double height)
    public Rectangle(Point2D origin, double width, double height, Plane plane)

    // Conversion Methods
    public Polyline ToPolyline()
    public Polygon ToPolygon()
}
```

#### Disc Class

Represents a filled circle.

**Key Features:**

-   **Geometric Properties**: Radius, center point, plane
-   **Boundary Access**: Get circle boundary
-   **Containment Testing**: Point-in-circle tests
-   **Boolean Operations**: Union, intersection, difference with other shapes

#### Polygon Class

A closed shape defined by a sequence of vertices.

### Collection Types

#### GeometryCollection<T> Class

A strongly-typed collection of geometry objects.

**Public API:**

```csharp
public class GeometryCollection<T> : BaseObject, IGeometry, ICollection<T>
    where T : IGeometry
{
    public int Count { get; }
    public bool IsReadOnly { get; }

    // Collection Operations
    public void Add(T item)
    public bool Remove(T item)
    public void Clear()
    public bool Contains(T item)

    // Geometry Operations
    public BoundingBox GetBoundingBox()
    public IGeometry Duplicate()
    public bool Transform(Transform transform)
}
```

**Usage Examples:**

-   Point collection: `var points = new GeometryCollection<Point3D>();`
-   Curve collection: `var curves = new GeometryCollection<ICurve>();`

### Intersection System

The library provides a sophisticated intersection system accessible through fluent API patterns:

**Pattern**: `geometryA.Intersection.With(geometryB, parameters...)`

**Examples:**

```csharp
// Line-Line intersection
bool intersects = line1.Intersection.With(line2, out Point3D point);
bool intersects = line1.Intersection.With(line2, out double paramA, out double paramB);

// Curve-Curve intersection
var intersections = curve1.Intersection.With(curve2);

// Shape-Shape intersection
var intersectionShape = shape1.Intersection.With(shape2);
```

**Intersection Types:**

-   **Intersection**: Actual crossing points or overlapping regions
-   **Proximity**: Closest approach between geometries
-   **Coincidence**: Overlapping or identical geometries

### Spatial Operations

#### Proximity Analysis

Find closest points between geometries:

```csharp
// Accessed via geometry.Proximity.With(...)
double distance = curve1.Proximity.With(curve2, out Point3D closestPoint1, out Point3D closestPoint2);
```

#### Coincidence Detection

Detect overlapping or identical geometries:

```csharp
// Accessed via geometry.Coincidence.With(...)
bool isCoincident = curve1.Coincidence.With(curve2);
```

---

## Complete API Summary

### Library Ecosystem Overview

The Aurecon.CoDe library ecosystem provides a comprehensive computational design and engineering toolkit with four core components:

1. **Aurecon.CoDe.Base** - Foundation types and utilities
2. **Aurecon.CoDe.Mathematics** - Mathematical operations and data structures
3. **Aurecon.CoDe.Geometry** - Geometry kernel with computational tools
4. **Aurecon.CoDe.Geometry.Serialization.Json** - JSON serialization framework

### Key Integration Patterns

#### Creating and Working with Geometry

```csharp
using Aurecon.CoDe.Base;
using Aurecon.CoDe.Geometry;
using Aurecon.CoDe.Geometry.Primitives;
using Aurecon.CoDe.Geometry.Curves;
using Aurecon.CoDe.Geometry.Shapes;

// Basic geometry creation
var point1 = new Point3D(0, 0, 0);
var point2 = new Point3D(10, 0, 0);
var line = new LineSegment(point1, point2);

// Complex geometry operations
var circle = new Circle(new Point3D(5, 0, 0), 3);
var intersections = line.Intersection.With(circle);

// Working with collections
var geometries = new GeometryCollection<IGeometry> { line, circle };
```

#### Mathematical Operations

```csharp
using Aurecon.CoDe.Mathematics;
using Aurecon.CoDe.Mathematics.Functions;

// Polynomial operations
var poly = new Polynomial(new[] { 1.0, 2.0, 3.0 }); // 1 + 2x + 3x²
double result = poly.Evaluate(2.0);
var derivative = poly.Differentiate();

// Matrix operations
var matrix = new Matrix(3, 3);
matrix[0, 0] = 1; matrix[1, 1] = 1; matrix[2, 2] = 1; // Identity
var inverse = matrix.Inverse();

// Domain operations
var domain = new Domain(0, 10);
var subdivided = domain.Split(5);
```

#### Serialization Workflows

```csharp
using Aurecon.CoDe.Geometry.Serialization.Json;

// Direct serialization
var line = new LineSegment(new Point3D(0, 0, 0), new Point3D(1, 1, 1));
string json = line.Serialize();

// Custom serialization
var serializer = new GeometrySerializer();
var complexGeometry = new Polyline(new[] { point1, point2, point3 });
string customJson = serializer.Serialize(complexGeometry);

// Deserialization
var deserializedLine = json.Deserialize<LineSegment>();
```

#### Storage and Property Management

```csharp
using Aurecon.CoDe.Base.Storage;

// Dynamic property access
var baseObj = new BaseObject();
baseObj["CustomProperty"] = "CustomValue";
baseObj["GeometryData"] = new Point3D(1, 2, 3);

// Type conversion
var convertedPoint = (Point3D)baseObj["GeometryData"];

// Property enumeration
foreach (var prop in baseObj.GetPropertyKeys())
{
    var value = baseObj[prop];
    // Process property
}
```

### Common Use Cases

#### Computational Design

-   Create parametric geometry using mathematical functions
-   Generate complex curves and surfaces with NURBS
-   Perform boolean operations on shapes and solids
-   Calculate intersections, projections, and transformations

#### Engineering Analysis

-   Measure distances, areas, and volumes
-   Analyze curve properties (curvature, tangents, normals)
-   Perform geometric queries and spatial analysis
-   Generate meshes for finite element analysis

#### Data Processing

-   Import/export geometry data via JSON serialization
-   Transform coordinate systems and apply geometric operations
-   Validate geometric constraints and tolerances
-   Process collections of geometric entities

#### Algorithmic Workflows

-   Implement shortest path algorithms on geometric graphs
-   Perform numerical integration and optimization
-   Apply interpolation and regression to geometric data
-   Create custom geometric algorithms using the kernel APIs

### Performance Considerations

1. **Memory Management**: Use `Duplicate()` methods for immutable operations
2. **Validation**: Check `IsValid` property before performing operations
3. **Optional Returns**: Use `Optional<T>` pattern for operations that may fail
4. **Collections**: Leverage `GeometryCollection<T>` for type-safe geometry groups
5. **Serialization**: Use appropriate serialization method based on data size and frequency

### Extension Points

The library provides several extension mechanisms:

1. **Custom Converters**: Implement `JsonConverter` for specialized serialization
2. **Type Mapping**: Register custom type conversions in `TypeMap`
3. **Property Modifiers**: Create custom serialization modifiers
4. **Collection Extensions**: Extend `IEnumerable<T>` with domain-specific operations
5. **Geometry Interfaces**: Implement `IGeometry`, `ICurve`, or `IShape` for custom types

This comprehensive system provides a solid foundation for computational design, engineering analysis, and geometric processing applications.
