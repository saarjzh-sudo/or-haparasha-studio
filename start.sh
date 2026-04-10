#!/bin/bash
# Start אור הפרשה Studio — frontend + backend

cd "$(dirname "$0")"

echo "🔥 Starting backend..."
cd backend
python3 -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

echo "🎨 Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Studio is running!"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
