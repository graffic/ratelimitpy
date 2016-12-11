import os
import pytest
from ratelimitpy.db import read_hotels_csv, HotelsRepository

@pytest.fixture
def dummy_csv(tmpdir):
    csv = tmpdir.join("dummy.csv")
    csv.write(
        "CITY,HOTELID,ROOM,PRICE\n" +
        "Bkk,1,Deluxe,1000\n" +
        "Bkk,2,Cheap,50\n" +
        "Ams,3,Cheap,100")
    return str(csv)

@pytest.fixture
def hotels(dummy_csv):
    return read_hotels_csv(dummy_csv)

def test_read_hotels_groups(hotels):
    assert len(hotels) == 2

def test_read_hotels_groups_in_list(hotels):
    assert len(hotels["Bkk"]) == 2

def test_read_hotels_sorts(hotels):
    assert [x.price for x in hotels["Bkk"]] == [50, 1000]

@pytest.fixture
def hotel_repo(dummy_csv):
    return HotelsRepository(dummy_csv)

hotels_repository_params = [
        (True, [50, 1000]),
        (False, [1000, 50])
]


class TestHotelRepository:
    @pytest.mark.parametrize("asc,res", hotels_repository_params)
    def test_get_by_city(self, hotel_repo, asc, res):
        assert [x.price for x in hotel_repo.get_by_city("Bkk", asc)] == res

