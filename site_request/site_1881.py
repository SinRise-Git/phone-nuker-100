from fake_useragent import UserAgent
class request:
    def __init__(self, phone_number, session):
        self.url = "https://sso.1881.no"
        self.phone_number = phone_number
        self.session = session
        self.headers = {"User-Agent": UserAgent().random}

    async def fetch_csrf_token(self):
        try:
            async with self.session.get(f"{self.url}/sso/login", headers=self.headers) as response:
                data = await response.text()
                if "CSRFtoken: '" not in data:
                    return False, f"Error at {self.fetch_csrf_token.__name__}: Did not find CSRF token in response"
                csrf_token = data.split("CSRFtoken: '")[1].split("'")[0]
                return True, csrf_token
        except Exception as e:
            return False, f"Error at {self.fetch_csrf_token.__name__}: {e}"
    
    async def send_sms(self):
        valid, response = await self.fetch_csrf_token()
        if valid:
            try:
                async with self.session.get(f"{self.url}/sso/getPin?phoneNo={self.phone_number}&CSRFtoken={response}", headers=self.headers) as response:
                    response_json = await response.json()
                    if response_json["pin_sent"] == "true":
                        return True, "SMS sent successfully", False
                    else:
                        return False, f"Error at {self.send_sms.__name__}: Failed to send SMS", response_json, 10
            except Exception as e:
                return False, f"Error at {self.send_sms.__name__}: {e}", 10
        else:
            return False, response, 10