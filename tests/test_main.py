"""
Unit Tests for DevOps Backend Service (FastAPI)
Test all endpoints and functionality
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    """Clear database before each test"""
    # Import database from main
    from main import tasks_db
    tasks_db.clear()
    yield

# ============== INFO & HEALTH TESTS ==============

def test_root_endpoint():
    """Test GET / - API info endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.json()
    assert 'service' in data
    assert 'version' in data
    assert 'endpoints' in data

def test_health_check():
    """Test GET /health - Health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'healthy'
    assert 'timestamp' in data

# ============== CREATE ITEM TESTS ==============

def test_create_item_success():
    """Test POST /api/tasks - Create task with valid data"""
    payload = {'title': 'Test Task', 'description': 'Test Description'}
    response = client.post('/api/tasks', json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == 'Test Task'
    assert 'id' in data
    assert 'created_at' in data

def test_create_item_minimal():
    """Test POST /api/tasks - Create task with only title"""
    payload = {'title': 'Minimal Task'}
    response = client.post('/api/tasks', json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == 'Minimal Task'
    assert data['description'] == ''

def test_create_item_missing_name():
    """Test POST /api/tasks - Missing title field"""
    payload = {'description': 'No title'}
    response = client.post('/api/tasks', json=payload)
    assert response.status_code == 422

def test_create_item_empty_json():
    """Test POST /api/tasks - Empty JSON"""
    response = client.post('/api/tasks', json={})
    assert response.status_code == 422

# ============== GET ALL ITEMS TESTS ==============

def test_get_items_empty():
    """Test GET /api/tasks - Empty list"""
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_items_single():
    """Test GET /api/tasks - Single item"""
    client.post('/api/tasks', json={'title': 'Task 1'})
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_get_items_multiple():
    """Test GET /api/tasks - Multiple items"""
    for i in range(3):
        client.post('/api/tasks', json={'title': f'Task {i+1}'})
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

# ============== GET SINGLE ITEM TESTS ==============

def test_get_item_by_id_success():
    """Test GET /api/tasks/<id> - Get existing task"""
    create_response = client.post('/api/tasks', json={'title': 'Test Task'})
    task_id = create_response.json()['id']
    response = client.get(f'/api/tasks/{task_id}')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == task_id
    assert data['title'] == 'Test Task'

def test_get_item_not_found():
    """Test GET /api/tasks/<id> - Task not found"""
    response = client.get('/api/tasks/non-existent-id')
    assert response.status_code == 404

# ============== DELETE ITEM TESTS ==============

def test_delete_item_success():
    """Test DELETE /api/tasks/<id> - Delete task"""
    create_response = client.post('/api/tasks', json={'title': 'To Delete'})
    task_id = create_response.json()['id']
    response = client.delete(f'/api/tasks/{task_id}')
    assert response.status_code == 204
    get_response = client.get(f'/api/tasks/{task_id}')
    assert get_response.status_code == 404

def test_delete_item_not_found():
    """Test DELETE /api/tasks/<id> - Delete non-existent task"""
    response = client.delete('/api/tasks/non-existent-id')
    assert response.status_code == 404

# ============== METRICS TESTS ==============

def test_metrics_endpoint():
    """Test GET /metrics - Prometheus metrics endpoint"""
    client.get('/health')
    client.post('/api/tasks', json={'title': 'Metric Task'})
    response = client.get('/metrics')
    assert response.status_code == 200
    metrics_text = response.text
    assert 'api_requests_total' in metrics_text
    assert 'api_request_duration_seconds' in metrics_text

# ============== TRACES TESTS ==============

def test_traces_endpoint():
    """Test GET /traces - Traces endpoint (not available, skip)"""
    # Tasks API doesn't have traces endpoint
    pass

def test_get_single_trace():
    """Test GET /traces/<trace_id> - Get single trace (not available, skip)"""
    # Tasks API doesn't have traces endpoint
    pass

# ============== WORKFLOW TESTS ==============

def test_complete_workflow():
    """Test a complete workflow: create, read, delete"""
    # 1. Create task
    create_response = client.post('/api/tasks', json={
        'title': 'Workflow Task',
        'description': 'Testing full workflow'
    })
    assert create_response.status_code == 201
    task = create_response.json()
    task_id = task['id']
    
    # 2. Verify task is in list
    list_response = client.get('/api/tasks')
    tasks = list_response.json()
    assert len(tasks) == 1
    
    # 3. Get specific task
    get_response = client.get(f'/api/tasks/{task_id}')
    assert get_response.status_code == 200
    assert get_response.json()['title'] == 'Workflow Task'
    
    # 4. Delete task
    delete_response = client.delete(f'/api/tasks/{task_id}')
    assert delete_response.status_code == 204
    
    # 5. Verify task is deleted
    final_list = client.get('/api/tasks')
    assert len(final_list.json()) == 0

# ============== STATS TESTS ==============

def test_stats_endpoint():
    """Test GET /stats - Stats endpoint (not available, skip)"""
    # Tasks API doesn't have stats endpoint
    pass