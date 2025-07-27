#!/bin/bash
# start.sh

# Activate virtual environment
source venv/Scripts/activate

# Run the FastAPI app with reload
uvicorn app.main:app --reload
