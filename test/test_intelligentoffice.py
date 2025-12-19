import unittest
from datetime import datetime
from unittest.mock import patch, Mock, PropertyMock
import mock.GPIO as GPIO
from mock.SDL_DS3231 import SDL_DS3231
from mock.adafruit_veml7700 import VEML7700
from src.intelligentoffice import IntelligentOffice, IntelligentOfficeError


class TestIntelligentOffice(unittest.TestCase):

    @patch.object(GPIO, "input")
    def test_worker_in_room_pin11(self, mock_pin_11: Mock):
        mock_pin_11.return_value = True
        io = IntelligentOffice()
        self.assertTrue(io.check_quadrant_occupancy(io.INFRARED_PIN1))

    @patch.object(GPIO, "input")
    def test_worker_in_room_pin12(self, mock_pin_2: Mock):
        mock_pin_2.return_value = True
        io = IntelligentOffice()
        self.assertTrue(io.check_quadrant_occupancy(io.INFRARED_PIN2))

    @patch.object(GPIO, "input")
    def test_worker_in_room_pin13(self, mock_pin_3: Mock):
        mock_pin_3.return_value = True
        io = IntelligentOffice()
        self.assertTrue(io.check_quadrant_occupancy(io.INFRARED_PIN3))

    @patch.object(GPIO, "input")
    def test_worker_in_room_pin15(self, mock_pin_4: Mock):
        mock_pin_4.return_value = True
        io = IntelligentOffice()
        self.assertTrue(io.check_quadrant_occupancy(io.INFRARED_PIN4))

    @patch.object(GPIO, "input")
    def test_wrong_pin_error(self, mock_pin_11: Mock):
        mock_pin_11.return_value = True
        io = IntelligentOffice()
        self.assertRaises(IntelligentOfficeError, io.check_quadrant_occupancy, 14)

    @patch.object(SDL_DS3231, "read_datetime")
    def test_blinds_fully_open_weekday(self, mock_datetime: Mock):
        mock_datetime.return_value = datetime(2025, 12, 19, 8, 10)
        io = IntelligentOffice()
        io.manage_blinds_based_on_time()
        self.assertTrue(io.blinds_open)

    @patch.object(SDL_DS3231, "read_datetime")
    def test_blinds_fully_close_weekend(self, mock_datetime: Mock):
        mock_datetime.return_value = datetime(2025, 12, 20, 8, 10)
        io = IntelligentOffice()
        io.manage_blinds_based_on_time()
        self.assertFalse(io.blinds_open)

    @patch.object(SDL_DS3231, "read_datetime")
    def test_blinds_fully_close_weekday_non_office_hours(self, mock_datetime: Mock):
        mock_datetime.return_value = datetime(2025, 12, 19, 20, 10)
        io = IntelligentOffice()
        io.manage_blinds_based_on_time()
        self.assertFalse(io.blinds_open)

    @patch.object(SDL_DS3231, "read_datetime")
    def test_blinds_fully_close_weekday_office_hours(self, mock_datetime: Mock):
        mock_datetime.return_value = datetime(2025, 12, 19, 17, 59)
        io = IntelligentOffice()
        io.manage_blinds_based_on_time()
        self.assertTrue(io.blinds_open)

    @patch.object(GPIO, "output")
    @patch.object(VEML7700, "lux", new_callable=PropertyMock)
    def test_light_on_lux(self, mock_lux: Mock, mock_led):
        mock_lux.side_effect = [501]
        io = IntelligentOffice()
        io.manage_light_level()
        mock_led.assert_called_with(io.LED_PIN, True)
        self.assertTrue(io.light_on)