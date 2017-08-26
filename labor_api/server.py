import asyncio
import logging
import json
import time

from aiohttp.web import Application, Response
from aiohttp_json_rpc import JsonRpc


class LaborApi:
    def __init__(self, loop=None, logger=None, state_file=None):
        self.loop = loop or asyncio.get_event_loop()
        self.logger = logger or logging.getLogger('labor-api')

        # setup rpc
        self.rpc = JsonRpc()

        self.rpc.add_topics(
            ('room-state'),
        )

        self.rpc.add_methods(
            ('', self.set_room_state),
        )

        # setup cache
        self.state_file = state_file

        self.cache = {
            'state': {
                'since': None,
                'open': None,
            },
            'archive': [],
            'responses': {
                'room': '',
                'room_archive': '',
            },
        }

        if not state_file:
            self.logger.debug('No state file.'
                              'rooms state will be closed by default')

            self._set_room_state(False)

        # setup app
        self.app = Application(loop=self.loop)

        # get room
        self.app.router.add_route('GET', '/api/room/', self.get_room)
        self.app.router.add_route('GET', '/api/room', self.get_room)

        # set room
        self.app.router.add_route('POST', '/api/room/', self.set_room)
        self.app.router.add_route('POST', '/api/room', self.set_room)

        # room archive
        self.app.router.add_route('GET', '/api/room_archive/',
                                  self.get_room_archive)

        self.app.router.add_route('GET', '/api/room_archive',
                                  self.get_room_archive)

        # websockets
        self.app.router.add_route('GET', '/api/rpc/', self.rpc)
        self.app.router.add_route('GET', '/api/rpc', self.rpc)

    def _set_room_state(self, open):
        self.logger.debug('set room state open=%s', open)

        state = {
            'since': int(time.time()),
            'open': bool(open),
        }

        self.cache['state'] = state

        self.cache['archive'].append({
            'lastchange': state['since'],
            'open': open,
        })

        self.cache['responses']['room'] = json.dumps(self.cache['state'])

        self.cache['responses']['room_archive'] = json.dumps(
            self.cache['archive'])

        # notify
        self.rpc.notify('room-state', state)

    def get_bool_from_str(self, str):
        if str.lower().strip() in ('1', 'true'):
            return True

        return False

    # methods
    async def set_room_state(self, request):
        self._set_room_state(request.params['open'])

        return self.cache['state']

    async def get_room(self, request):
        self.logger.debug('LaborApi.get_room(%s)', request)

        response = Response(text=self.cache['responses']['room'],
                            content_type='application/json')

        response.headers['Access-Control-Allow-Origin'] = '*'

        return response

    async def set_room(self, request):
        data = await request.post()

        self.logger.debug('LaborApi.set_room(%s(%s))', request, data)

        open = self.get_bool_from_str(data['open'])
        self._set_room_state(open=open)

        return Response(content_type='application/json',
                        text=json.dumps({
                            'success': True,
                            'status': '',
                        }))

    async def get_room_archive(self, request):
        self.logger.debug('LaborApi.get_room_archive(%s)', request)

        return Response(text=self.cache['responses']['room_archive'],
                        content_type='application/json')
