import pytest
from app.services.product import ProductService
from app.schemas.products import ProductCreationReq, ProductResp
from app.models.products import Product
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

@pytest.fixture
def mock_session():
    class MockSession:
        async def add(self, obj):
            # Simulate DB setting an ID
            obj.id = int(1)
            return obj
            
        async def commit(self):
            pass
            
        async def refresh(self, obj):
            # Simulate refreshing the object with DB data
            obj.created_at = datetime.now()
            obj.updated_at = datetime.now()
            pass
    
    return MockSession()

@pytest.fixture
def mock_repository(monkeypatch):
    class MockProductRepository:
        def __init__(self):
            self.model = Product

        async def create(self, session, data):
            # Create a new product instance
            db_obj = Product(
                id=int(1),  # Set ID explicitly
                name=data.name,
                description=data.description,
                price=data.price,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            # Add to_dict method
            async def to_dict():
                return {
                    "id": db_obj.id,
                    "name": db_obj.name,
                    "description": db_obj.description,
                    "price": db_obj.price,
                    "created_at": db_obj.created_at,
                    "updated_at": db_obj.updated_at
                }
            
            db_obj.to_dict = to_dict
            await session.add(db_obj)
            await session.refresh(db_obj)
            return db_obj

    # Mock the repository
    monkeypatch.setattr("app.repositories.product.ProductRepository", MockProductRepository)
    return MockProductRepository()

@pytest.mark.asyncio
async def test_create_product_service(mock_repository, mock_session):
    service = ProductService()
    product_data = ProductCreationReq(
        name="Test Product",
        description="Test Description",
        price=int(100)
    )
    
    result = await service.create_product(
        session=mock_session,
        product_data=product_data
    )
    
    assert isinstance(result, ProductResp)
    assert result.id == int(1) 
    assert result.name == "Test Product"
    assert result.description == "Test Description"
    assert result.price == int(100)
    assert result.created_at is not None
    assert result.updated_at is not None