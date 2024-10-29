import pytest
from app.repositories.product import ProductRepository
from app.models.products import Product
from app.schemas.products import ProductCreationReq

@pytest.fixture
def mock_db_session():
    class MockSession:
        async def add(self, obj):
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
    product_data = ProductCreationReq(
        name="Test Product",
        description="Test Description",
        price=100
    )
    
    result = await repository.create(mock_db_session, product_data)
    
    assert isinstance(result, Product)
    assert result.name == "Test Product" 