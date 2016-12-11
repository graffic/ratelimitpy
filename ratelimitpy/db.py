import csv


def read_hotels_csv(filename):
    """Build an dictionary with hotels

    The dictionary key is the city and it contains the hotels sorted by price
    """
    hotels = {}
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        # Skip header
        next(reader)
        for row in reader:
            hotel = Hotel(row[0], row[1], row[2], int(row[3]))
            city_hotels = hotels.get(hotel.city, [])
            city_hotels.append(hotel)
            hotels[hotel.city] = city_hotels

    for city in hotels:
        hotels[city].sort(key=lambda x: x.price)

    return hotels


class Hotel:
    def __init__(self, city, hotel_id, room, price):
        self.city = city
        self.hotel_id = hotel_id
        self.room = room
        self.price = price


class HotelsRepository:
    def __init__(self, filename):
        self.__hotels = read_hotels_csv(filename)

    def get_by_city(self, city, ascending):
        hotels = self.__hotels.get(city, [])
        if not ascending:
            return hotels[::-1]
        return hotels
