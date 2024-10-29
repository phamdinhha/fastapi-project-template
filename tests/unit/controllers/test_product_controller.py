import pytest
from app.api.http.products import create_product
from app.schemas.products import ProductCreationReq, ProductResp

@pytest.fixture
def mock_service(monkeypatch):
    class MockProductService:
        async def create_product(self, session, product_data):
            # Return mock data
            return ProductResp(
                id=1,
                name=product_data.name,
                created_at="2024-01-01T00:00:00",
                updated_at="2024-01-01T00:00:00"
            )
    
    monkeypatch.setattr("app.api.http.products.ProductService", MockProductService)
    return MockProductService()

@pytest.mark.asyncio
async def test_create_product_controller(mock_service):
    product_data = ProductCreationReq(name="Test Product", description="Test Description", price=100, config={"key": "value"})
    
    result = await create_product(product_data, session=None)
    
    assert result.id == 1
    assert result.name == "Test Product" 
    assert result.description == "Test Description"
    assert result.price == 100
    assert result.config == {"key": "value"}