# To-Do List REST API (FastAPI)

A simple To-Do List REST API built with **FastAPI**. Data is stored in-memory in a Python list (no database).

## Task Model
```json
{
  "id": 1,
  "title": "Finish Python assignment",
  "completed": false
}
```

## Setup

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Server runs at: `http://127.0.0.1:8000`

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints

| Method | Endpoint       | Description                    |
|--------|----------------|---------------------------------|
| POST   | /todos         | Create a new task               |
| GET    | /todos         | Retrieve all tasks              |
| GET    | /todos/{id}    | Retrieve a task by ID           |
| PUT    | /todos/{id}    | Update a task (title/completed) |
| DELETE | /todos/{id}    | Delete a task                   |

## Sample Requests

**Create a task**
```bash
curl -X POST http://127.0.0.1:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Finish Python assignment"}'
```

**Get all tasks**
```bash
curl http://127.0.0.1:8000/todos
```

**Get a task by ID**
```bash
curl http://127.0.0.1:8000/todos/1
```

**Update a task**
```bash
curl -X PUT http://127.0.0.1:8000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

**Delete a task**
```bash
curl -X DELETE http://127.0.0.1:8000/todos/1
```

## Testing
- All endpoints can be tested via **Postman** (import the OpenAPI spec from `http://127.0.0.1:8000/openapi.json`, or hit endpoints directly).
- Interactive testing is also available via **Swagger UI** at `/docs`.
