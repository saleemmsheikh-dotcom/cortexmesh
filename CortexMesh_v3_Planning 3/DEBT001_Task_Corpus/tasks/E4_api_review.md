# E4 REST API Design Review

## Task ID
E4

## Title
REST API Design Review

## Objective
Review the proposed API specification and identify security, maintainability, and design concerns.

## API Specification

### Create User
`POST /users`

Request:
```json
{
  "username": "alice",
  "email": "alice@example.com",
  "role": "admin"
}
```

Response:
```json
{
  "id": 123,
  "username": "alice"
}
```

### Get User
`GET /users/{id}`

Response:
```json
{
  "id": 123,
  "username": "alice",
  "email": "alice@example.com",
  "role": "admin"
}
```

## Required Output
1. Security concerns
2. Data validation concerns
3. Authorization concerns
4. Maintainability concerns
5. Recommended improvements

## Evaluation Focus
Architectural review consistency and recommendation stability.

## External Dependencies
None.
