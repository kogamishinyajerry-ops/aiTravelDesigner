"""
Models package
"""
from .user import User
from .destination import Destination
from .attraction import Attraction
from .restaurant import Restaurant
from .itinerary import Itinerary

__all__ = [
    "User",
    "Destination",
    "Attraction",
    "Restaurant",
    "Itinerary",
]
