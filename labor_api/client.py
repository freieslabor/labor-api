import json

from aiohttp import ClientSession


class LaborApiClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_session = ClientSession()

    def __del__(self):
        del self.client_session

    async def get_room_state(self):
        url = 'http://{}:{}/api/room/'.format(self.host, self.port)

        async with self.client_session.get(url) as response:
            response_data = json.loads(await response.text())

            return response_data['open'], response_data['since']

    async def set_room_state(self, open):
        url = 'http://{}:{}/api/room/'.format(self.host, self.port)
        data = {'open': bool(open)}

        async with self.client_session.post(url, data=data) as response:
            response_data = json.loads(await response.text())

            return response_data['success'], response_data['status']
