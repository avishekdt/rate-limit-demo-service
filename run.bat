:: run.bat

@echo off
REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the FastAPI app with reload
uvicorn app.main:app --reload
