import pytest
from app.services.product import ProductService
from app.schemas.products import ProductCreationReq
from app.models.products import Product

@pytest.fixture
def mock_repository(monkeypatch):
    class MockProductRepository:
        async def create(self, session, data):
            # Return mock model
            mock_product = Product()
            mock_product.id = 1
            mock_product.name = data.name
            mock_product.created_at = "2024-01-01T00:00:00"
            mock_product.updated_at = "2024-01-01T00:00:00"
            return mock_product
    
    monkeypatch.setattr("app.services.product.ProductRepository", MockProductRepository)
    return MockProductRepository()

@pytest.mark.asyncio
async def test_create_product_service(mock_repository):
    service = ProductService()
    product_data = ProductCreationReq(name="Test Product")
    
    result = await service.create_product(session=None, product_data=product_data)
    
    assert result.name == "Test Product" 