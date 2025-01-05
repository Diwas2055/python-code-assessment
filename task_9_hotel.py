from datetime import datetime
from typing import Optional, List

hotels_db = {}
bookings_db = {}
reviews_db = {}


class Room:
    def __init__(
        self, room_id: int, hotel_id: int, room_type: str, price_per_night: float
    ):
        self.room_id = room_id
        self.hotel_id = hotel_id
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.is_available = True

    def update_availability(self, available: bool):
        self.is_available = available

    def dynamic_pricing(self) -> float:
        """Returns the dynamic price based on availability."""
        return (
            self.price_per_night * 1.2
            if not self.is_available
            else self.price_per_night
        )


class Hotel:
    def __init__(self, hotel_id: int, name: str, location: str):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms = []

    def add_room(self, room: Room):
        """Adds a room to the hotel."""
        self.rooms.append(room)
        hotels_db[self.hotel_id] = self

    def search_rooms(
        self,
        check_in_date: datetime,
        check_out_date: datetime,
        room_type: Optional[str] = None,
    ) -> List[Room]:
        """Search for available rooms."""
        available_rooms = [
            (room, room.dynamic_pricing())
            for room in self.rooms
            if room.is_available and (room_type is None or room.room_type == room_type)
        ]
        return available_rooms


class Booking:
    def __init__(
        self,
        booking_id: int,
        user_id: int,
        hotel_id: int,
        room_id: int,
        check_in_date: datetime,
        check_out_date: datetime,
    ):
        self.booking_id = booking_id
        self.user_id = user_id
        self.hotel_id = hotel_id
        self.room_id = room_id
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.booking_date = datetime.now()
        self.status = "Confirmed"

    def cancel(self):
        """Cancel the booking."""
        self.status = "Cancelled"
        bookings_db[self.booking_id] = self

    def modify(self, new_check_in_date: datetime, new_check_out_date: datetime):
        """Modify the booking dates."""
        self.check_in_date = new_check_in_date
        self.check_out_date = new_check_out_date
        self.status = "Modified"
        bookings_db[self.booking_id] = self


class Review:
    def __init__(self, hotel_id: int, user_id: int, rating: int, comment: str):
        self.hotel_id = hotel_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment

    def submit_review(self):
        """Submit a review for the hotel."""
        if self.hotel_id not in reviews_db:
            reviews_db[self.hotel_id] = []
        reviews_db[self.hotel_id].append(self)


class Payment:
    def __init__(self, user_id: int, booking_id: int, amount: float):
        self.user_id = user_id
        self.booking_id = booking_id
        self.amount = amount
        self.payment_date = datetime.now()

    def process_payment(self) -> bool:
        """Process payment for a booking."""
        print(f"Processing payment of ${self.amount} for booking {self.booking_id}")
        return True  # Mocking a successful payment


# Factory Methods for Room and Hotel Creation
def create_hotel() -> Hotel:
    name = input("Enter hotel name: ")
    location = input("Enter hotel location: ")
    hotel_id = len(hotels_db) + 1
    hotel = Hotel(hotel_id, name, location)
    print(f"Hotel '{name}' created with ID {hotel_id}.")
    return hotel


def create_room(hotel: Hotel) -> Room:
    room_type = input("Enter room type (Single/Double/Suite): ")
    price_per_night = float(input(f"Enter price per night for {room_type}: "))
    room_id = len(hotel.rooms) + 1
    room = Room(room_id, hotel.hotel_id, room_type, price_per_night)
    hotel.add_room(room)
    print(f"Room {room_type} created with ID {room_id}.")
    return room


def search_rooms() -> None:
    hotel_id = int(input("Enter hotel ID to search for rooms: "))
    check_in_date = datetime.strptime(
        input("Enter check-in date (YYYY-MM-DD): "), "%Y-%m-%d"
    )
    check_out_date = datetime.strptime(
        input("Enter check-out date (YYYY-MM-DD): "), "%Y-%m-%d"
    )
    room_type = input(
        "Enter room type to filter by (Single/Double/Suite) or leave empty for no filter: "
    )

    hotel = hotels_db.get(hotel_id)
    if hotel:
        rooms = hotel.search_rooms(check_in_date, check_out_date, room_type)
        if rooms:
            print(f"\nAvailable rooms at {hotel.name} for your selected dates:")
            for room, price in rooms:
                print(
                    f"Room {room.room_type} (ID: {room.room_id}) - ${price} per night"
                )
        else:
            print("No available rooms for your selected dates.")
    else:
        print("Hotel not found.")


def make_booking() -> None:
    hotel_id = int(input("Enter hotel ID to book: "))
    room_id = int(input("Enter room ID to book: "))
    check_in_date = datetime.strptime(
        input("Enter check-in date (YYYY-MM-DD): "), "%Y-%m-%d"
    )
    check_out_date = datetime.strptime(
        input("Enter check-out date (YYYY-MM-DD): "), "%Y-%m-%d"
    )

    hotel = hotels_db.get(hotel_id)
    if hotel:
        room = next((r for r in hotel.rooms if r.room_id == room_id), None)
        if room and room.is_available:
            booking_id = len(bookings_db) + 1
            booking = Booking(
                booking_id, 101, hotel_id, room_id, check_in_date, check_out_date
            )
            bookings_db[booking.booking_id] = booking
            room.update_availability(False)
            print(f"Booking confirmed! Booking ID: {booking.booking_id}")
            payment = Payment(101, booking.booking_id, room.dynamic_pricing())
            if payment.process_payment():
                print("Payment successful!")
        else:
            print("Room is not available.")
    else:
        print("Hotel not found.")


def cancel_booking() -> None:
    booking_id = int(input("Enter booking ID to cancel: "))
    booking = bookings_db.get(booking_id)
    if booking:
        booking.cancel()
        print(f"Booking {booking_id} has been cancelled.")
    else:
        print("Booking not found.")


def modify_booking() -> None:
    booking_id = int(input("Enter booking ID to modify: "))
    booking = bookings_db.get(booking_id)
    if booking:
        new_check_in_date = datetime.strptime(
            input("Enter new check-in date (YYYY-MM-DD): "), "%Y-%m-%d"
        )
        new_check_out_date = datetime.strptime(
            input("Enter new check-out date (YYYY-MM-DD): "), "%Y-%m-%d"
        )
        booking.modify(new_check_in_date, new_check_out_date)
        print(f"Booking {booking_id} has been modified.")
    else:
        print("Booking not found.")


def submit_review() -> None:
    hotel_id = int(input("Enter hotel ID to review: "))
    rating = int(input("Enter your rating (1 to 5): "))
    comment = input("Enter your comment: ")
    review = Review(hotel_id, 101, rating, comment)
    review.submit_review()
    print("Review submitted.")


# Main Program Loop
while True:
    print("\nHotel Booking System Menu:")
    print("1. Create Hotel")
    print("2. Create Room")
    print("3. Search Rooms")
    print("4. Make Booking")
    print("5. Cancel Booking")
    print("6. Modify Booking")
    print("7. Submit Review")
    print("8. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        create_hotel()
    elif choice == "2":
        create_room(hotels_db.get(len(hotels_db), None))
    elif choice == "3":
        search_rooms()
    elif choice == "4":
        make_booking()
    elif choice == "5":
        cancel_booking()
    elif choice == "6":
        modify_booking()
    elif choice == "7":
        submit_review()
    elif choice == "8":
        break
    else:
        print("Invalid option. Please try again.")
