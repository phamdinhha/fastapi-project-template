import pytest
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.http.products import create_product
from app.schemas.products import ProductCreationReq, ProductResp
from app.services.product import ProductService

@pytest.fixture
def mock_service(monkeypatch):
    class MockProductService:
        async def create_product(self, session, product_data):
            return ProductResp(
                id=1,
                name=product_data.name,
                description=product_data.description,
                price=product_data.price,
                created_at="2024-01-01T00:00:00",
                updated_at="2024-01-01T00:00:00"
            )

    # Mock the Depends injection
    async def mock_get_service():
        return MockProductService()

    monkeypatch.setattr(
        "app.api.http.products.Depends", 
        lambda _: mock_get_service()
    )
    return MockProductService()

@pytest.mark.asyncio
async def test_create_product_controller(mock_service):
    product_data = ProductCreationReq(
        name="Test Product",
        description="Test Description",
        price=100
    )
    
    # Create a mock session
    mock_session = AsyncSession()
    
    # Create a mock service instance
    mock_service_instance = mock_service
    
    result = await create_product(
        product=product_data,
        session=mock_session,
        service=mock_service_instance  # Pass the actual mock service instance
    )
    
    assert result.id == 1
    assert result.name == "Test Product"
    assert result.description == "Test Description"
    assert result.price == 100