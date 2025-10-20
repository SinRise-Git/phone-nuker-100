import os
import inspect
from fake_useragent import UserAgent

class Request:
    def __init__(self, phone_number, session):
        self.url = "https://mobilbillett.skyss.no"
        self.phone_number = phone_number
        self.session = session
        self.headers = {"User-Agent": UserAgent().random}    
        self.file_name = os.path.basename(__file__)

    async def send_sms(self):
        data = {
            "mobileCc":"47",
            "mobileNumber":self.phone_number
        }
        try:
            async with self.session.post(f"{self.url}/api/frontend/rest/pinchallenge", json=data, headers=self.headers) as response:
                if response.status != 200:
                    return False, f"Error in {self.file_name} at line {inspect.currentframe().f_lineno}: Status {response.status}", 60
                json_response = await response.json()
                success = json_response.get('retrieved')
                if success:
                    return True, f"SMS sent successfully to +47{self.phone_number} from skyss.no", None
                else:
                    return False, f"Error in {self.file_name} at line {inspect.currentframe().f_lineno}: SMS not sent", 60
             
        except Exception as e:
            return False, f"Error in {self.file_name} at line {inspect.currentframe().f_lineno}: {e}", 60