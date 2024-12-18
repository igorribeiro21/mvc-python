from unittest import mock
import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.people import PeopleTable
from .people_repository import PeopleRepository

class MockConnection:
    def __init__(self):
        self.session = UnifiedAlchemyMagicMock(
            data=[
                (
                    [mock.call.add(PeopleTable), mock.call.query(PeopleTable)], #query
                    [
                        PeopleTable(first_name="first name", last_name="last name", age=24, pet_id=1)
                    ] #resultado
                )
            ]
        )

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass

class MockConnectionNoResult:
    def __init__(self):
        self.session = UnifiedAlchemyMagicMock()
        self.session.add.side_effect = self.__raise_no_result_found
        self.session.query.side_effect = self.__raise_no_result_found

    def __raise_no_result_found(self, *args, **kwargs):
        raise NoResultFound("No result found")

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass

def test_insert_person():
    mock_connection = MockConnection()
    repo = PeopleRepository(mock_connection)

    first_name = "test name"
    last_name = "test last"
    age = 26
    pet_id = 2

    repo.insert_person(first_name, last_name, age, pet_id)

    mock_connection.session.add.assert_called_once()
    mock_connection.session.commit.assert_called_once()

def test_insert_person_error():
    mock_connection = MockConnectionNoResult()
    repo = PeopleRepository(mock_connection)

    with pytest.raises(Exception):
        first_name = "test name"
        last_name = "test last"
        age = 26
        pet_id = 2

        repo.insert_person(first_name, last_name, age, pet_id)

    mock_connection.session.rollback.assert_called_once()

def test_get_person():
    mock_connection = MockConnection()
    repo = PeopleRepository(mock_connection)

    repo.get_person(1)

    mock_connection.session.query.assert_called_once_with(PeopleTable)
    mock_connection.session.outerjoin.assert_called_once()

def test_get_person_error():
    mock_connection = MockConnectionNoResult()
    repo = PeopleRepository(mock_connection)

    response = repo.get_person(1)

    assert response is None
