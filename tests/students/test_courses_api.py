import pytest
from rest_framework.test import APIClient
from model_bakery import baker
import sys
from django_testing import settings
from students.models import Course, Student

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_first_course_addition(client, course_factory):
    courses = course_factory(name='Python')
    response = client.get(f'/api/v1/courses/{courses.id}/')
    assert response.status_code == 200
    assert response.json()['name'] == 'Python'

@pytest.mark.django_db    
def test_get_proper_courses(client, course_factory):
    courses = course_factory(_quantity=15)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    assert len(response.json()) == 15
    assert courses[0].id == response.json()[0]['id']
    assert courses[0].name == response.json()[0]['name']
    
@pytest.mark.django_db      
def test_courses_id_filtration(client, course_factory):
    courses = course_factory(_quantity=15)
    response = client.get(f'/api/v1/courses/?id={courses[5].id}')
    assert response.status_code == 200
    assert response.json()[0]['id'] == courses[5].id
    
@pytest.mark.django_db    
def test_course_creation(client):
    response = client.post(path='/api/v1/courses/', data={'name': 'Python'})
    assert response.status_code == 201
    assert response.json()['name'] == 'Python'
    
@pytest.mark.django_db    
def test_course_update(client, course_factory):
    courses = course_factory(name='Python')
    response = client.patch(path='/api/v1/courses/'+ str(courses.id) + '/', data={'name': 'Java'})
    assert response.status_code == 200
    assert response.json()['name'] == 'Java'
    
@pytest.mark.django_db    
def test_course_delete(client, course_factory):
    courses = course_factory(name='Python')
    response = client.delete(f'/api/v1/courses/{str(courses.id)}/')
    assert response.status_code == 204


    
    
    
    