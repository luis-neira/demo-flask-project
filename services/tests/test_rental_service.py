import sqlite3
import pytest
from unittest.mock import MagicMock

from services import RentalService


@pytest.fixture
def mock_db():
    """Creates an in-memory SQLite database and a mocked Database object."""
    mock_conn = sqlite3.connect(":memory:")  # In-memory database
    mock_conn.row_factory = sqlite3.Row
    mock_cursor = mock_conn.cursor()

    # Create a mock rentals table
    mock_cursor.execute("""
        CREATE TABLE rentals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            location TEXT,
            price INTEGER
        )
    """)
    mock_conn.commit()

    # Create a fake Database instance
    mock_db_instance = MagicMock()
    mock_db_instance.conn = mock_conn
    mock_db_instance.cursor = mock_cursor

    yield mock_db_instance  # Provide it to tests

    mock_conn.close()  # Clean up after tests


@pytest.fixture
def rental_service(mock_db):
    """Provide an instance of RentalService with a mocked database."""
    return RentalService(db=mock_db)


def test_add_one(rental_service, mock_db):
    """Test adding a rental."""
    new_rental = {"name": "Cozy Apartment",
                  "location": "Downtown", "price": 1200}

    result = rental_service.add_one(new_rental)

    assert result["id"] == 1
    assert result["name"] == "Cozy Apartment"
    assert result["location"] == "Downtown"
    assert result["price"] == 1200


def test_get_all(rental_service, mock_db):
    """Test retrieving all rentals."""
    mock_db.cursor.execute("INSERT INTO rentals (name, location, price) VALUES (?, ?, ?)",
                           ("Test Rental", "City Center", 1500))
    mock_db.conn.commit()

    result = rental_service.get_all()

    assert len(result) == 1
    assert result[0]["name"] == "Test Rental"
    assert result[0]["location"] == "City Center"
    assert result[0]["price"] == 1500


def test_get_one_by_id(rental_service, mock_db):
    """Test retrieving a rental by ID."""
    mock_db.cursor.execute("INSERT INTO rentals (name, location, price) VALUES (?, ?, ?)",
                           ("Beach House", "Seaside", 2000))
    mock_db.conn.commit()

    result = rental_service.get_one_by_id(1)

    assert result is not None
    assert result["name"] == "Beach House"


def test_delete_one_by_id(rental_service, mock_db):
    """Test deleting a rental by ID."""
    mock_db.cursor.execute("INSERT INTO rentals (name, location, price) VALUES (?, ?, ?)",
                           ("Mountain Cabin", "Hills", 900))
    mock_db.conn.commit()

    assert rental_service.exists(1) is True

    success = rental_service.delete_one_by_id(1)

    assert success is True
    assert rental_service.exists(1) is False


def test_update_one_by_id(rental_service, mock_db):
    """Test updating a rental."""
    mock_db.cursor.execute("INSERT INTO rentals (name, location, price) VALUES (?, ?, ?)",
                           ("Small Apartment", "Uptown", 800))
    mock_db.conn.commit()

    updated_data = {"name": "Updated Apartment", "price": 1000}
    result = rental_service.update_one_by_id(1, updated_data)

    assert result is not None
    assert result["name"] == "Updated Apartment"
    assert result["price"] == 1000
