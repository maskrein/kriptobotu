@echo off
cd /d C:\Users\enes\crypto_ai

echo Starting PNL Worker...

C:\Users\enes\ABD_Borsa_Robotu\venv\Scripts\python.exe -c "from runtime.pnl_worker import start_pnl_worker; start_pnl_worker(); print('PNL WORKER STARTED')"

echo Starting Dashboard...

C:\Users\enes\ABD_Borsa_Robotu\venv\Scripts\python.exe -m uvicorn app.web_dashboard_server:app --host 0.0.0.0 --port 8000

pause
