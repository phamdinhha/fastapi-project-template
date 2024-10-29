import pytest
from app.repositories.product import ProductRepository
from app.models.products import Product

@pytest.fixture
def mock_db_session(monkeypatch):
    class MockSession:
        async def add(self, obj):
            # Simulate adding to DB
            obj.id = 1
            return obj
            
        async def commit(self):
            pass
            
        async def refresh(self, obj):
            pass
    
    return MockSession()

@pytest.mark.asyncio
async def test_create_product_repository(mock_db_session):
    repository = ProductRepository()
    product_data = {"name": "Test Product"}
    
    result = await repository.create(mock_db_session, product_data)
    
    assert isinstance(result, Product)
    assert result.name == "Test Product" 