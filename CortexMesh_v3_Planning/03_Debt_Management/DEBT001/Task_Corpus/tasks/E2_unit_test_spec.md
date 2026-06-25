# E2 Unit Test Suite Design

## Task ID
E2

## Title
Unit Test Suite Design

## Objective
Design a comprehensive unit test suite for the provided function specification.

## Function Specification
Function Name: `calculate_discount`

Inputs:
- `price` (float)
- `discount_percent` (float)

Behavior:
- Returns discounted price
- Discount must be between 0 and 100 inclusive
- Negative prices are invalid
- Output rounded to 2 decimal places

Examples:
```python
calculate_discount(100, 10) -> 90.00
calculate_discount(50, 0) -> 50.00
calculate_discount(80, 100) -> 0.00
```

Invalid Inputs:
```python
calculate_discount(-10, 20)
calculate_discount(100, -5)
calculate_discount(100, 120)
```

## Required Output
1. Normal test cases
2. Boundary test cases
3. Invalid input test cases
4. Edge cases
5. Coverage assessment

## Evaluation Focus
Coverage recommendation consistency and reasoning stability.

## External Dependencies
None.
