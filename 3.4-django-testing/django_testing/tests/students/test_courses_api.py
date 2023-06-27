import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture()
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_course(client, courses_factory, students_factory):
    students = students_factory(_quantity=3)
    course = courses_factory(name='python', students=students)
    response = client.get(f'/api/v1/courses/{course.id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'python'
    assert len(data['students']) == 3


@pytest.mark.django_db
def test_get_courses_list(client, courses_factory):
    courses = courses_factory(_quantity=3)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, c in enumerate(data):
        assert c['name'] == courses[i].name


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'name': 'typescript'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_update_course(client, courses_factory):
    course = courses_factory(name='python')
    response = client.patch(f"/api/v1/courses/{course.id}/", data={'name': 'typescript'})
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'typescript'


@pytest.mark.django_db
def test_delete_course(client, courses_factory):
    course = courses_factory(name='python')
    count = Course.objects.count()
    response = client.delete(f"/api/v1/courses/{course.id}/")
    assert response.status_code == 204
    assert Course.objects.count() == count - 1


@pytest.mark.django_db
def test_courses_filter_by_id(client, courses_factory):
    courses = courses_factory(_quantity=3)
    id = courses[2].id
    # response = client.get(f"/api/v1/courses/?id={id}")
    response = client.get("/api/v1/courses/", {'id': id})

    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == id


@pytest.mark.django_db
def test_courses_filter_by_name(client, courses_factory):
    courses = courses_factory(_quantity=3)
    name = courses[2].name
    response = client.get("/api/v1/courses/", {'name': name})
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == name
