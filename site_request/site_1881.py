import os
import inspect
from fake_useragent import UserAgent

class Request:
    def __init__(self, phone_number, session):
        self.url = "https://sso.1881.no"
        self.phone_number = phone_number
        self.session = session
        self.headers = {"User-Agent": UserAgent().random}
        self.file_name = os.path.basename(__file__)

    async def fetch_csrf_token(self):
        try:
            async with self.session.get(f"{self.url}/sso/login", headers=self.headers) as http_response:
                if http_response.status != 200:
                    return False, f"Error in  at line {inspect.currentframe().f_lineno}: Status {http_response.status}", 60
                data = await http_response.text()
                if "CSRFtoken: '" not in data:
                    return False, f"Error in {self.file_name} at line {inspect.currentframe().f_lineno}: Did not find CSRF token in response", 60
                csrf_token = data.split("CSRFtoken: '")[1].split("'")[0]
                return True, csrf_token, None
        except Exception as e:
            return False, f"Error in {self.file_name} at line {inspect.currentframe().f_lineno}: {e}", 60

    async def send_sms(self):
        method_name = self.send_sms.__name__
        sent, response, retry  = await self.fetch_csrf_token()
        if not sent:
            return False, response, retry
        try:
            async with self.session.get(f"{self.url}/sso/getPin?phoneNo={self.phone_number}&CSRFtoken={response}", headers=self.headers) as response:
                if response.status != 200:
                    return False, f"Error at {self.file_name}: Status {response.status}", 60
                response_json = await response.json()
                success = response_json.get("pin_sent")
                if success:
                    return True, f"SMS sent successfully to +47{self.phone_number} from 1881.no", False
                else:
                    return False, f"Error in {self.file_name} at line {inspect.currentframe().f_lineno}: Failed to send SMS", response_json, 60
        except Exception as e:
            return False, f"Error in {self.file_name} at line {inspect.currentframe().f_lineno}: {e}", 60