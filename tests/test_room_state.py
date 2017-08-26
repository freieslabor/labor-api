import pytest


@pytest.mark.asyncio
async def test_get_room(labor_api_context):
    open, since = await labor_api_context.client.get_room_state()

    assert not open

    await labor_api_context.client.set_room_state(True)
    open, since = await labor_api_context.client.get_room_state()

    assert open
