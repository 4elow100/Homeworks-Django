import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def course_factory(student_factory):
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_course(client, course_factory):
    course = course_factory()

    response = client.get(f'/api/v1/courses/{course.id}/')

    assert response.status_code == 200
    assert response.json()['id'] == course.id


@pytest.mark.django_db
def test_get_courses_list(client, course_factory):
    course = course_factory(_quantity=10)

    response = client.get(f'/api/v1/courses/')

    assert response.status_code == 200
    assert len(response.json()) == 10


@pytest.mark.django_db
def test_courses_filter_by_id(client, course_factory, student_factory):
    course = course_factory(_quantity=10)

    response = client.get(f'/api/v1/courses/?id={course[2].id}')

    assert response.status_code == 200
    assert response.json()[0]['id'] == course[2].id


@pytest.mark.django_db
def test_courses_filter_by_name(client, course_factory, student_factory):
    course = course_factory(_quantity=10)

    response = client.get(f'/api/v1/courses/?name={course[5].name}')

    assert response.status_code == 200
    assert response.json()[0]['name'] == course[5].name


@pytest.mark.django_db
def test_course_create(client, student_factory):
    student = student_factory()

    response = client.post('/api/v1/courses/', data={'name': 'Django', 'students': [student.id]})

    assert response.status_code == 201
    assert response.json()['name'] == 'Django'


@pytest.mark.django_db
def test_course_update(client, course_factory):
    course = course_factory(_quantity=10)

    response = client.patch(f'/api/v1/courses/{course[4].id}/', data={'name': 'Django'})

    assert response.status_code == 200
    assert response.json()['name'] == 'Django'


@pytest.mark.django_db
def test_course_delete(client, course_factory):
    course = course_factory(_quantity=10)
    courses_count = Course.objects.count()

    response = client.delete(f'/api/v1/courses/{course[8].id}/')

    assert response.status_code == 204
    assert Course.objects.count() == courses_count - 1
