import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_within_limit():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/ping")
        assert response.status_code == 200
        assert response.headers.get("X-RateLimit-Limit") is not None


@pytest.mark.asyncio
async def test_exceed_limit():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        for _ in range(5):  # within limit
            await ac.get("/ping")
        response = await ac.get("/ping")  # exceed limit
        assert response.status_code == 429
        assert "Retry-After" in response.headers


@pytest.mark.asyncio
async def test_headers_on_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/ping")
        assert "X-RateLimit-Limit" in response.headers
        assert "X-RateLimit-Remaining" in response.headers
