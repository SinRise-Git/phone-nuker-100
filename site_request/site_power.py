from fake_useragent import UserAgent

class Request:
    def __init__(self, phone_number, session):
        self.url = "https://www.power.no"
        self.phone_number = phone_number
        self.session = session
        self.headers = {"User-Agent": UserAgent().random}

    async def generate_id(self):
        method_name = self.generate_id.__name__
        data = {"username": f"+47{self.phone_number}"}
        try:
            async with self.session.post(f"{self.url}/api/v2/mypower/recovery/start-login", json=data, headers=self.headers) as http_response:
                if http_response.status != 200:
                    return False, f"Error at {method_name}: HTTP {http_response.status}", 60
                json_response = await http_response.json()
                user_id = json_response.get('value', {}).get('id')
                if user_id:
                    return True, user_id, None
                else:
                    return False, f"Error at {method_name}: No ID found in response", 60
        except Exception as e:
            return False, f"Error at {method_name}: Failed sending request: {e}", 60

    async def send_sms(self):
        method_name = self.send_sms.__name__
        sent, result, retry = await self.generate_id()
        if not sent:
            return False, result, retry
        data = {
            "id": result,
            "username": f"+47{self.phone_number}"
        }
        try:
            async with self.session.post(f"{self.url}/api/v2/mypower/recovery/login-resend", json=data, headers=self.headers) as http_response:
                if http_response.status != 200:
                    return False, f"Error at {method_name}: HTTP {http_response.status}", 60
                json_response = await http_response.json()
                success = json_response.get('value', {}).get('success')
                if success:
                    return True, http_response, None
                else:
                    return False, f"Error at {method_name}: SMS not sent", 60
        except Exception as e:
            return False, f"Error at {method_name}: Failed sending request: {e}", 60