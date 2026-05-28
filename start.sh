#!/bin/sh
python app/services/training_service.py
uvicorn app.main:app --host 0.0.0.0 --port $PORT