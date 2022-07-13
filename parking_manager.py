import re

from db_manager import DBManager
from ocr_space import OcrSpace

mongodb_url = 'mongodb://localhost:27017'


class ParkingManager:
    def __init__(self, api_key):
        self.ocr_space = OcrSpace(api_key)
        self.db_manager = DBManager(mongodb_url)
        self.access_block_postfix = ("85", "86", "87", "88", "89", "00")
        self.access_block_7_digits = ("0", "5")
        self.access_approve_postfix = ("25", "26")

    def extract_license_plate_number(self, file_image):
        parsed_result_json = self.ocr_space.ocr_space_file(filename=file_image)
        parsed_result = re.search(pattern="\"ParsedText\":\"(.*?)\"", string=parsed_result_json).group(1)
        number = ''.join(c for c in parsed_result if c.isdigit())
        return number

    def is_car_approved_to_access(self, file_image):
        plate_number = self.extract_license_plate_number(file_image=file_image)

        if (plate_number.endswith(self.access_block_postfix)):
            self.report_decision_to_db(plate_number=plate_number, is_approved=False)
            return False

        if (len(plate_number) == 7 and plate_number.endswith(self.access_block_7_digits)):
            self.report_decision_to_db(plate_number=plate_number, is_approved=False)
            return False

        if (plate_number.endswith(self.access_approve_postfix)):
            self.report_decision_to_db(plate_number=plate_number, is_approved=True)
            return True


    def report_decision_to_db(self, plate_number, is_approved):
        self.db_manager.add_decision_to_database(plate_number=plate_number, is_approved=is_approved)


if __name__ == '__main__':
    parking_manager = ParkingManager(api_key="K89700208888957")
    is_approved = parking_manager.is_car_approved_to_access(file_image="plate.png")
    if (is_approved):
        print(True)
    else:
        print(False)
    parking_manager.db_manager.client.close()
