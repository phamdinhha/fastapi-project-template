echo "Starting server..."
echo "----------RUNNING MIGRATIONS----------"
alembic upgrade head
echo "----------RUNNING SERVER--------------"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4