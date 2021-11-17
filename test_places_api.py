import unittest
from places_api import getPlaceInfo


class TestPlaceData(unittest.TestCase):
    # ensure api returns a real address
    def test_address(self):
        self.assertEqual(
            getPlaceInfo("village burger")["address"],
            "5649 Stone Rd, Centreville, VA 20120, United States",
            "address failed",
        )

    # ensure api returns a real latitude value
    def test_latitude(self):
        self.assertAlmostEqual(
            getPlaceInfo("dunwoody tavern")["lat"], 33.9476607, "latitude failed"
        )

    # ensure api returns a real latitude value
    def test_longitude(self):
        self.assertAlmostEqual(
            getPlaceInfo("card kingdom")["lon"], -122.3805333, "longitude failed"
        )

    # ensure api returns a real name
    def test_name(self):
        self.assertEqual(
            getPlaceInfo("vermack pool")["name"],
            "Vermack Swim and Tennis Club",
            "name failed",
        )
