"""
DevOps Backend Service - Task Management REST API with FastAPI
Implements observability (metrics, logs, tracing)
Lines of code: ~140
"""
import time
import uuid
import logging
from datetime import datetime
from typing import Optional, List, Dict

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest
from pythonjsonlogger import jsonlogger

# ============== INITIALIZATION ==============
app = FastAPI(
    title="DevOps Backend",
    version="1.0.0",
    description="Task Management REST API with observability"
)

# ============== LOGGING SETUP ==============
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# ============== METRICS SETUP ==============
request_count = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'api_request_duration_seconds',
    'API request latency',
    ['method', 'endpoint']
)

tasks_created = Counter('tasks_created_total', 'Total tasks created')

# ============== PYDANTIC MODELS ==============
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""

class Task(BaseModel):
    id: str
    title: str
    description: str
    status: str
    created_at: str

# ============== IN-MEMORY DATABASE ==============
tasks_db: Dict[str, dict] = {}

# ============== MIDDLEWARE ==============
@app.middleware("http")
async def add_observability(request: Request, call_next):
    """Middleware for observability (metrics, logs, tracing)"""
    request.state.start_time = time.time()
    request.state.trace_id = str(uuid.uuid4())
    
    logger.info('HTTP Request', extra={
        'trace_id': request.state.trace_id,
        'method': request.method,
        'path': request.url.path,
    })
    
    try:
        response = await call_next(request)
        duration = time.time() - request.state.start_time
        
        request_count.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        request_duration.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        logger.info('HTTP Response', extra={
            'trace_id': request.state.trace_id,
            'status_code': response.status_code,
            'duration_ms': round(duration * 1000, 2)
        })
        
        response.headers['X-Request-ID'] = request.state.trace_id
        return response
    except Exception as e:
        logger.error('HTTP Error', extra={
            'trace_id': request.state.trace_id,
            'error': str(e)
        })
        raise

# ============== API ENDPOINTS ==============
@app.get("/")
async def index():
    """API Information"""
    return {
        "service": "DevOps Backend",
        "version": "1.0.0",
        "endpoints": {
            "GET /health": "Health check",
            "GET /api/tasks": "List all tasks",
            "POST /api/tasks": "Create task",
            "GET /api/tasks/{id}": "Get task by ID",
            "PUT /api/tasks/{id}": "Update task",
            "DELETE /api/tasks/{id}": "Delete task",
            "GET /metrics": "Prometheus metrics",
            "GET /docs": "API documentation (Swagger UI)"
        }
    }

@app.get("/health")
async def health():
    """Health Check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/tasks", response_model=List[Task])
async def get_tasks():
    """Get all tasks"""
    logger.info('Fetching all tasks', extra={'total': len(tasks_db)})
    return list(tasks_db.values())

@app.post("/api/tasks", response_model=Task, status_code=201)
async def create_task(task: TaskCreate, request: Request):
    """Create new task"""
    if not task.title:
        logger.warning('Invalid task request - missing title')
        raise HTTPException(status_code=400, detail="Title is required")
    
    task_id = str(uuid.uuid4())
    new_task = {
        "id": task_id,
        "title": task.title,
        "description": task.description or "",
        "status": "pending",
        "created_at": datetime.utcnow().isoformat()
    }
    tasks_db[task_id] = new_task
    tasks_created.inc()
    
    logger.info('Task created', extra={
        'trace_id': request.state.trace_id,
        'task_id': task_id,
        'title': task.title
    })
    
    return new_task

@app.get("/api/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str, request: Request):
    """Get task by ID"""
    if task_id not in tasks_db:
        logger.warning('Task not found', extra={
            'trace_id': request.state.trace_id,
            'task_id': task_id
        })
        raise HTTPException(status_code=404, detail="Task not found")
    
    return tasks_db[task_id]

@app.put("/api/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task: TaskCreate, request: Request):
    """Update task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    existing_task = tasks_db[task_id]
    if task.title:
        existing_task['title'] = task.title
    if task.description:
        existing_task['description'] = task.description
    
    logger.info('Task updated', extra={
        'trace_id': request.state.trace_id,
        'task_id': task_id
    })
    
    return existing_task

@app.delete("/api/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str, request: Request):
    """Delete task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    del tasks_db[task_id]
    
    logger.info('Task deleted', extra={
        'trace_id': request.state.trace_id,
        'task_id': task_id
    })
    
    return None

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(
        content=generate_latest(),
        media_type="text/plain; charset=utf-8"
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error('Unhandled Exception', extra={
        'trace_id': getattr(request.state, 'trace_id', 'unknown'),
        'error': str(exc)
    })
    return {"error": "Internal server error"}

if __name__ == "__main__":
    import uvicorn
    logger.info('Starting DevOps Backend Service with FastAPI')
    uvicorn.run(app, host="localhost", port=5000)