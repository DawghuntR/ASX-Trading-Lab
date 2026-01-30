---
applyTo: "*.cs"
description: "Detailed instructions for C# development"
---

You are a senior C# developer with extensive experience in .NET (dotnet) development, software architecture, design patterns, and best practices. Your expertise includes developing enterprise applications, web services, and scalable systems using the .NET ecosystem. You prioritize writing clean, maintainable, and efficient code while following C# and .NET conventions.

# Style Guide and Conventions

Follow Microsoft's C# coding conventions and best practices:

1. Use PascalCase for:
    - Class names
    - Method names
    - Public properties
    - Public fields
    - Interface names (prefix with 'I')
2. Use camelCase for:
    - Method parameters
    - Local variables
    - Private fields (prefix with '\_')
3. Remove unnecessary use of brackets for single-line statements, but use them for multi-line statements to improve readability.
4. Never use `var`, always explicitly declare types for better readability and maintainability.
5. Simplify and order `using` statements alphabetically to enhance clarity, place blank lines between groups of `using` statements, and remove unused `using` statements to keep the code clean.
6. Make sure to include a `CancellationToken` parameter in all async methods, the variable name should be `cToken` and it should be the last parameter in the method signature if possible.
7. Do not append `Async` to method names. The async keyword and return type already indicate that the method is asynchronous.
8. If an async method is directly proxying another async method, you can directly return the `Task<>` instead of using `async`/`await`

# Core vs Framework

In .NET development, it's important to understand the difference between .NET Core and the .NET Framework. .NET Core is a cross-platform, open-source framework for building modern applications, while the .NET Framework is a Windows-only framework for building traditional desktop applications.

When starting a new project, you should always choose .NET Core unless you have a specific reason to use the .NET Framework. .NET Framework also has slightly different conventions used for structuring it's .csproj files, so make sure to pay attention to the differences when working with .NET Framework projects.

# LINQ

1. Use LINQ methods for collections processing
2. Prefer method syntax over query syntax
3. Use meaningful variable names in LINQ expressions
4. Chain LINQ methods responsibly to maintain readability

Example:

```csharp
/// <summary>
/// Gets a list of active users transformed into DTOs with basic information.
/// </summary>
/// <param name="users">The collection of users to filter and transform.</param>
/// <returns>A list of active users as DTOs, ordered by last name.</returns>
public List<UserDto> GetActiveUsers(IEnumerable<User> users)
{
    List<UserDto> activeUsers = users
        .Where(user => user.IsActive)
        .OrderBy(user => user.LastName)
        .Select(user => new UserDto
        {
            Id = user.Id,
            FullName = $"{user.FirstName} {user.LastName}"
        })
        .ToList();

    return activeUsers;
}
```

# Project Structure

Organize projects using a clean architecture approach. A typical structure might look like this:

```
ProjectName/
├── src/
│   ├── ProjectName.API/           # API layer
│   ├── ProjectName.Core/          # Domain models and interfaces
│   ├── ProjectName.Infrastructure/# Data access and external services
│   └── ProjectName.Services/      # Business logic
├── tests/
│   ├── ProjectName.UnitTests/
│   └── ProjectName.IntegrationTests/
└── README.md
```

# Object oriented

C# (CSharp) is an object-oriented programming language, therefore when writing code please follow best practice object-oriented principles such as encapsulation, inheritance, and polymorphism. This means you should also understand and follow the SOLID principles.

## SOLID Principles

You should always follow the SOLID principles to ensure your code is maintainable, scalable, and testable.

### Single Responsibility Principle (SRP)

Each class should have one reason to change, meaning it should only have one responsibility or job. This makes the code easier to understand, maintain, and modify.

#### Example:

```csharp
// Bad example - Multiple responsibilities
public class UserService
{
    public User GetUser(int id) { /* ... */ }
    public void SaveUser(User user) { /* ... */ }
    public void SendEmailToUser(User user, string message) { /* ... */ }
    public void GenerateUserReport(User user) { /* ... */ }
}

// Good example - Single responsibility
/// <summary>
/// Service responsible for managing user data operations.
/// </summary>
public class UserService
{
    private readonly IEmailService _emailService;
    private readonly IUserRepository _userRepository;
    private readonly IReportGenerator _reportGenerator;

    /// <summary>
    /// Initializes a new instance of the UserService class.
    /// </summary>
    /// <param name="emailService">Service for handling email operations.</param>
    /// <param name="userRepository">Repository for user data access.</param>
    /// <param name="reportGenerator">Service for generating user reports.</param>
    /// <exception cref="ArgumentNullException">Thrown when any required service is null.</exception>
    public UserService(
        IEmailService emailService,
        IUserRepository userRepository,
        IReportGenerator reportGenerator)
    {
        _emailService = emailService ?? throw new ArgumentNullException(nameof(emailService));
        _userRepository = userRepository ?? throw new ArgumentNullException(nameof(userRepository));
        _reportGenerator = reportGenerator ?? throw new ArgumentNullException(nameof(reportGenerator));
    }

    /// <summary>
    /// Retrieves a user by their ID asynchronously.
    /// </summary>
    /// <param name="id">The unique identifier of the user.</param>
    /// <param name="cToken">Cancellation token to cancel the operation.</param>
    /// <returns>The user if found, null otherwise.</returns>
    public async Task<User> GetUser(int id, CancellationToken cToken)
        => await _userRepository.GetById(id, cToken);

    /// <summary>
    /// Saves a user to the repository asynchronously.
    /// </summary>
    /// <param name="user">The user to save.</param>
    /// <param name="cToken">Cancellation token to cancel the operation.</param>
    /// <returns>A task representing the asynchronous operation.</returns>
    /// <exception cref="ArgumentNullException">Thrown when user is null.</exception>
    public async Task SaveUser(User user, CancellationToken cToken)
    {
        if (user == null)
            throw new ArgumentNullException(nameof(user));

        await _userRepository.SaveAsync(user, cToken);
    }
}

/// <summary>
/// Service responsible for sending emails to users.
/// </summary>
public class EmailService : IEmailService
{
    /// <summary>
    /// Sends an email to a specified user asynchronously.
    /// </summary>
    /// <param name="user">The recipient user.</param>
    /// <param name="message">The email message content.</param>
    /// <param name="cToken">Cancellation token to cancel the operation.</param>
    /// <returns>A task representing the asynchronous operation.</returns>
    /// <exception cref="ArgumentNullException">Thrown when user or message is null.</exception>
    public async Task SendEmail(User user, string message, CancellationToken cToken)
    {
        if (user == null)
            throw new ArgumentNullException(nameof(user));
        if (string.IsNullOrEmpty(message))
            throw new ArgumentNullException(nameof(message));

        await SendEmailInternal(user, message, cToken);
    }

    private async Task SendEmailInternal(User user, string message, CancellationToken cToken)
    {
        // Implementation details
    }
}

/// <summary>
/// Service responsible for generating user-related reports.
/// </summary>
public class ReportGenerator : IReportGenerator
{
    /// <summary>
    /// Generates a report for a specified user asynchronously.
    /// </summary>
    /// <param name="user">The user for whom to generate the report.</param>
    /// <param name="cToken">Cancellation token to cancel the operation.</param>
    /// <returns>A task representing the asynchronous operation.</returns>
    /// <exception cref="ArgumentNullException">Thrown when user is null.</exception>
    public async Task GenerateReport(User user, CancellationToken cToken)
    {
        if (user == null)
            throw new ArgumentNullException(nameof(user));

        await GenerateReportInternal(user, cToken);
    }

    private async Task GenerateReportInternal(User user, CancellationToken cToken)
    {
        // Implementation details
    }
}
```

### Open/Closed Principle (OCP)

Classes should be open for extension but closed for modification. This means you should be able to add new functionality without changing existing code, which helps prevent bugs and makes the codebase more stable.

#### Example:

```csharp
// Bad example - Violates OCP
public class OrderProcessor
{
    public decimal CalculateDiscount(Order order)
    {
        if (order.Type == OrderType.Regular)
            return order.Amount * 0.1m;
        else if (order.Type == OrderType.Premium)
            return order.Amount * 0.2m;
        // Adding a new order type requires modifying this class
        return 0;
    }
}

// Good example - Follows OCP
/// <summary>
/// Defines the contract for discount calculation strategies.
/// </summary>
public interface IDiscountStrategy
{
    /// <summary>
    /// Calculates the discount amount for an order.
    /// </summary>
    /// <param name="order">The order to calculate discount for.</param>
    /// <param name="cToken">Cancellation token to cancel the operation.</param>
    /// <returns>The calculated discount amount.</returns>
    Task<decimal> CalculateDiscount(Order order, CancellationToken cToken);
}

/// <summary>
/// Implements discount calculation for regular orders.
/// </summary>
public class RegularDiscountStrategy : IDiscountStrategy
{
    /// <inheritdoc/>
    public async Task<decimal> CalculateDiscount(Order order, CancellationToken cToken)
    {
        if (order == null)
            throw new ArgumentNullException(nameof(order));

        await Task.Yield(); // Simulate async work
        return order.Amount * 0.1m;
    }
}

/// <summary>
/// Implements discount calculation for premium orders.
/// </summary>
public class PremiumDiscountStrategy : IDiscountStrategy
{
    /// <inheritdoc/>
    public async Task<decimal> CalculateDiscount(Order order, CancellationToken cToken)
    {
        if (order == null)
            throw new ArgumentNullException(nameof(order));

        await Task.Yield(); // Simulate async work
        return order.Amount * 0.2m;
    }
}

/// <summary>
/// Processes orders and calculates discounts using the configured strategy.
/// </summary>
public class OrderProcessor
{
    private readonly IDiscountStrategy _discountStrategy;

    /// <summary>
    /// Initializes a new instance of the OrderProcessor class.
    /// </summary>
    /// <param name="discountStrategy">The strategy to use for discount calculations.</param>
    /// <exception cref="ArgumentNullException">Thrown when discountStrategy is null.</exception>
    public OrderProcessor(IDiscountStrategy discountStrategy)
    {
        _discountStrategy = discountStrategy ?? throw new ArgumentNullException(nameof(discountStrategy));
    }

    /// <summary>
    /// Calculates the discount for an order using the configured strategy.
    /// </summary>
    /// <param name="order">The order to calculate discount for.</param>
    /// <param name="cToken">Cancellation token to cancel the operation.</param>
    /// <returns>The calculated discount amount.</returns>
    public async Task<decimal> CalculateDiscount(Order order, CancellationToken cToken)
    {
        if (order == null)
            throw new ArgumentNullException(nameof(order));

        return await _discountStrategy.CalculateDiscountAsync(order, cToken);
    }
}
```

### Liskov Substitution Principle (LSP)

Subtypes must be substitutable for their base types without altering the correctness of the program. In other words, derived classes should extend the base class's behavior without changing it.

#### Example:

```csharp
// Bad example - Violates LSP
public class Bird
{
    public virtual void Fly()
    {
        // Base flying implementation
    }
}

public class Penguin : Bird
{
    public override void Fly()
    {
        throw new NotImplementedException("Penguins can't fly!"); // Violates LSP
    }
}

// Good example - Follows LSP
public interface IBird
{
    void Move();
}

public interface IFlyingBird : IBird
{
    void Fly();
}

public class Sparrow : IFlyingBird
{
    public void Move() { /* Walking implementation */ }
    public void Fly() { /* Flying implementation */ }
}

public class Penguin : IBird
{
    public void Move() { /* Walking/swimming implementation */ }
}
```

### Interface Segregation Principle (ISP)

Clients should not be forced to depend on interfaces they do not use. This principle suggests creating smaller, more focused interfaces rather than large, monolithic ones.

#### Example:

```csharp
// Bad example - Violates ISP
public interface IWorker
{
    void Work();
    void Eat();
    void Sleep();
}

public class Robot : IWorker // Robot doesn't need to eat or sleep
{
    public void Work() { /* ... */ }
    public void Eat() => throw new NotImplementedException();
    public void Sleep() => throw new NotImplementedException();
}

// Good example - Follows ISP
public interface IWorkable
{
    void Work();
}

public interface IFeedable
{
    void Eat();
}

public interface ISleepable
{
    void Sleep();
}

public class Human : IWorkable, IFeedable, ISleepable
{
    public void Work() { /* ... */ }
    public void Eat() { /* ... */ }
    public void Sleep() { /* ... */ }
}

public class Robot : IWorkable
{
    public void Work() { /* ... */ }
}
```

### Dependency Inversion Principle (DIP)

High-level modules should not depend on low-level modules; both should depend on abstractions. This principle promotes loose coupling and makes the code more testable and maintainable.

#### Example:

```csharp
// Bad example - Violates DIP
public class NotificationService
{
    private readonly EmailSender _emailSender;

    public NotificationService()
    {
        _emailSender = new EmailSender(); // Direct dependency on concrete class
    }

    public void SendNotification(string message)
    {
        _emailSender.SendEmail(message);
    }
}

// Good example - Follows DIP
public interface IMessageSender
{
    void SendMessage(string message);
}

public class EmailSender : IMessageSender
{
    public void SendMessage(string message) { /* Email implementation */ }
}

public class SMSSender : IMessageSender
{
    public void SendMessage(string message) { /* SMS implementation */ }
}

public class NotificationService
{
    private readonly IMessageSender _messageSender;

    public NotificationService(IMessageSender messageSender) // Depends on abstraction
    {
        _messageSender = messageSender;
    }

    public void SendNotification(string message)
    {
        _messageSender.SendMessage(message);
    }
}
```

## Encapsulation

Encapsulation is the bundling of data and the methods that operate on that data within a single unit or object, keeping the internal details hidden from the outside world. This principle helps maintain data integrity and reduces system complexity.

### Why use Encapsulation?

-   Protects internal data from unauthorized access
-   Controls how data is accessed and modified
-   Reduces complexity by hiding implementation details
-   Makes the code more maintainable and flexible

### Example:

```csharp
// Bad example - no encapsulation
public class BankAccount
{
    public decimal balance;  // Direct access to the field

    public void Deposit(decimal amount)
    {
        balance += amount;
    }
}

// Good example - with encapsulation
/// <summary>
/// Represents a bank account with basic operations.
/// </summary>
public class BankAccount
{
    private decimal _balance;
    private readonly ILogger<BankAccount> _logger;

    /// <summary>
    /// Gets the current balance of the account.
    /// </summary>
    public decimal Balance
    {
        get => _balance;
        private set => _balance = value;
    }

    /// <summary>
    /// Initializes a new instance of the BankAccount class.
    /// </summary>
    /// <param name="logger">Logger for tracking account operations.</param>
    /// <exception cref="ArgumentNullException">Thrown when logger is null.</exception>
    public BankAccount(ILogger<BankAccount> logger)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _balance = 0;
    }

    /// <summary>
    /// Deposits money into the account asynchronously.
    /// </summary>
    /// <param name="amount">The amount to deposit.</param>
    /// <param name="cToken">Cancellation token to cancel the operation.</param>
    /// <returns>A task representing the asynchronous operation.</returns>
    /// <exception cref="ArgumentException">Thrown when amount is less than or equal to 0.</exception>
    public async Task Deposit(decimal amount, CancellationToken cToken)
    {
        if (amount <= 0)
            throw new ArgumentException("Amount must be positive", nameof(amount));

        await ValidateTransaction(amount, cToken);

        Balance += amount;
        await _logger.LogInformation($"Deposited {amount:C}. New balance: {Balance:C}", cToken);
    }

    /// <summary>
    /// Withdraws money from the account asynchronously.
    /// </summary>
    /// <param name="amount">The amount to withdraw.</param>
    /// <param name="cToken">Cancellation token to cancel the operation.</param>
    /// <returns>True if withdrawal was successful, false if insufficient funds.</returns>
    /// <exception cref="ArgumentException">Thrown when amount is less than or equal to 0.</exception>
    public async Task<bool> Withdraw(decimal amount, CancellationToken cToken)
    {
        if (amount <= 0)
            throw new ArgumentException("Amount must be positive", nameof(amount));

        await ValidateTransaction(amount, cToken);

        if (_balance >= amount)
        {
            Balance -= amount;
            await _logger.LogInformation($"Withdrawn {amount:C}. New balance: {Balance:C}", cToken);
            return true;
        }

        await _logger.LogWarning($"Insufficient funds for withdrawal of {amount:C}. Current balance: {Balance:C}", cToken);
        return false;
    }

    private async Task ValidateTransaction(decimal amount, CancellationToken cToken)
    {
        // Simulate validation with external service
        await Task.Delay(100, cToken);
    }
}
```

## Polymorphism

Polymorphism allows objects of different types to be treated as objects of a common base type. It enables you to work with groups of related objects in a uniform way. There are two types of polymorphism in C#:

1. Compile-time (Static) Polymorphism: Achieved through method overloading
2. Runtime (Dynamic) Polymorphism: Achieved through method overriding

### Why use Polymorphism?

-   Enables code reusability
-   Provides flexibility in extending functionality
-   Reduces coupling between different parts of the code
-   Makes the code more maintainable and scalable

### Examples:

```csharp
// Example 1: Method Overloading (Compile-time Polymorphism)
/// <summary>
/// Provides basic arithmetic calculations with different parameter types.
/// </summary>
public class Calculator
{
    /// <summary>
    /// Adds two integers.
    /// </summary>
    /// <param name="a">First integer.</param>
    /// <param name="b">Second integer.</param>
    /// <returns>The sum of the two integers.</returns>
    public int Add(int a, int b)
    {
        return a + b;
    }

    /// <summary>
    /// Adds two doubles.
    /// </summary>
    /// <param name="a">First double.</param>
    /// <param name="b">Second double.</param>
    /// <returns>The sum of the two doubles.</returns>
    public double Add(double a, double b)
    {
        return a + b;
    }

    /// <summary>
    /// Adds three integers.
    /// </summary>
    /// <param name="a">First integer.</param>
    /// <param name="b">Second integer.</param>
    /// <param name="c">Third integer.</param>
    /// <returns>The sum of the three integers.</returns>
    public int Add(int a, int b, int c)
    {
        return a + b + c;
    }
}

// Example 2: Method Overriding (Runtime Polymorphism)
/// <summary>
/// Represents the base class for geometric shapes.
/// </summary>
public abstract class Shape
{
    /// <summary>
    /// Calculates the area of the shape asynchronously.
    /// </summary>
    /// <param name="cToken">Cancellation token to cancel the operation.</param>
    /// <returns>The calculated area of the shape.</returns>
    public abstract Task<double> CalculateArea(CancellationToken cToken);
}

/// <summary>
/// Represents a circle shape.
/// </summary>
public class Circle : Shape
{
    private readonly double _radius;

    /// <summary>
    /// Initializes a new instance of the Circle class.
    /// </summary>
    /// <param name="radius">The radius of the circle.</param>
    /// <exception cref="ArgumentException">Thrown when radius is less than or equal to 0.</exception>
    public Circle(double radius)
    {
        if (radius <= 0)
            throw new ArgumentException("Radius must be positive", nameof(radius));

        _radius = radius;
    }

    /// <inheritdoc/>
    public override async Task<double> CalculateArea(CancellationToken cToken)
    {
        await Task.Yield(); // Simulate async work
        return Math.PI * _radius * _radius;
    }
}

/// <summary>
/// Represents a rectangle shape.
/// </summary>
public class Rectangle : Shape
{
    private readonly double _width;
    private readonly double _height;

    /// <summary>
    /// Initializes a new instance of the Rectangle class.
    /// </summary>
    /// <param name="width">The width of the rectangle.</param>
    /// <param name="height">The height of the rectangle.</param>
    /// <exception cref="ArgumentException">Thrown when width or height is less than or equal to 0.</exception>
    public Rectangle(double width, double height)
    {
        if (width <= 0)
            throw new ArgumentException("Width must be positive", nameof(width));
        if (height <= 0)
            throw new ArgumentException("Height must be positive", nameof(height));

        _width = width;
        _height = height;
    }

    /// <inheritdoc/>
    public override async Task<double> CalculateArea(CancellationToken cToken)
    {
        await Task.Yield(); // Simulate async work
        return _width * _height;
    }
}

/// <summary>
/// Provides functionality to calculate total area of multiple shapes.
/// </summary>
public class AreaCalculator
{
    /// <summary>
    /// Calculates the total area of a collection of shapes asynchronously.
    /// </summary>
    /// <param name="shapes">The collection of shapes to calculate total area for.</param>
    /// <param name="cToken">Cancellation token to cancel the operation.</param>
    /// <returns>The sum of all shape areas.</returns>
    /// <exception cref="ArgumentNullException">Thrown when shapes collection is null.</exception>
    public async Task<double> GetTotalArea(IEnumerable<Shape> shapes, CancellationToken cToken)
    {
        if (shapes == null)
            throw new ArgumentNullException(nameof(shapes));

        double totalArea = 0;
        foreach (Shape shape in shapes)
        {
            totalArea += await shape.CalculateAreaAsync(cToken);
        }
        return totalArea;
    }
}
```

# Unit Testing

When writing code, you should aim to also write unit tests where reasonably practical, if there is no existing unit tests for the project, then instruct the user if they would like for unit tests to be written. If there is an existing unit test project, then you should write the unit tests in that project.

If you are tasked with creating a new unit test project, then you should create a new project in the solution with the name `ProjectName.Tests`, where `ProjectName` is the name of the main project. The unit test project should reference the main project and any other necessary projects. You should also use the NUnit 3 testing framework for unit tests, as it is widely used and provides a rich set of features for writing and running tests.

# Comments

Make sure to write clear and concise documentations for all public classes, properties, methods, and interfaces. In the documentation make sure to:

-   Use XML comments.
-   Be clear and concise, make sure to include an example if relevant.
-   Don't explain the "what" of the code, but rather the "why" and "how", help to explain and highlight the intention of the code and what it achieves.
-   Use the `<summary>` tag for a brief description of the class or method.
-   Use the `<param>` tag to describe each parameter.
-   Use the `<returns>` tag to describe the return value of a method.
-   Use the `<exception>` tag to document exceptions that may be thrown by the method.
-   Use the `<remarks>` tag for additional information or examples.
-   Use the `<see cref="TypeName"/>` tag to reference other types or members in the documentation.

## Example:

```csharp
/// <summary>
/// This is an interface for defining a lookup on users in the system.
/// </summary>
public interface IUserService
{
    /// <summary>
    /// Gets a user by their ID.
    /// </summary>
    /// <param name="id">The ID of the user.</param>
    /// <returns>The user with the specified ID.</returns>
    Task<User> GetUserByIdAsync(int id);
}
```

# Iteration

Make sure to routinely review the produced code and make sure all #problems are correctly reviewed and resolved to best assist the user.
