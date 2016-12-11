from flask.json import JSONEncoder
from ratelimitpy.db import Hotel


def hotel_encode(hotel):
    return {
        "City": hotel.city,
        "HotelID": hotel.hotel_id,
        "Room": hotel.room,
        "Price": hotel.price
    }


class AppJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Hotel):
            return hotel_encode(obj)
        return super(AppJSONEncoder, self).default(obj)
