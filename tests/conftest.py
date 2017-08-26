import pytest

from labor_api.server import LaborApi
from labor_api.client import LaborApiClient


class LaborApiContext:
    def __init__(self, server, client):
        self.server = server
        self.client = client


@pytest.yield_fixture
def labor_api_context(event_loop, unused_tcp_port):
    labor_api = LaborApi()
    client = LaborApiClient(host='localhost', port=unused_tcp_port)
    context = LaborApiContext(server=labor_api, client=client)

    # setup server
    handler = labor_api.app.make_handler()
    server = event_loop.run_until_complete(
        event_loop.create_server(handler, 'localhost', unused_tcp_port)
    )

    yield context

    # teardown
    async def teardown():
        await server.wait_closed()
        await labor_api.app.shutdown()
        await handler.finish_connections(1)
        await labor_api.app.cleanup()

    del context.client

    server.close()
    event_loop.run_until_complete(teardown())
