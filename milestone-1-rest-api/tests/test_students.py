from app import create_app, db


def test_healthcheck(client):
    response = client.get('/api/v1/healthcheck')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'


def test_add_student(client):
    response = client.post('/api/v1/students', json={
        'name': 'Kumar Prafful',
        'age': 22,
        'email': 'add@gmail.com'
    })
    assert response.status_code == 201
    assert response.json['name'] == 'Kumar Prafful'


def test_get_students(client):
    response = client.get('/api/v1/students')
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_get_student_not_found(client):
    response = client.get('/api/v1/students/999')
    assert response.status_code == 404
    assert response.json['error'] == 'Student not found'


def test_update_student(client):
    post_response = client.post('/api/v1/students', json={
        'name': 'Kumar Prafful',
        'age': 22,
        'email': 'update@gmail.com'
    })
    student_id = post_response.json['id']
    response = client.put(f'/api/v1/students/{student_id}', json={
        'name': 'Prafful Kumar',
        'age': 23
    })
    assert response.status_code == 200
    assert response.json['name'] == 'Prafful Kumar'


def test_delete_student(client):
    post_response = client.post('/api/v1/students', json={
        'name': 'Kumar Prafful',
        'age': 22,
        'email': 'delete@gmail.com'
    })
    student_id = post_response.json['id']
    response = client.delete(f'/api/v1/students/{student_id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Student deleted successfully'