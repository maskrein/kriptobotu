@echo off
cd /d C:\Users\enes\crypto_ai

echo ======================================
echo CRYPTO AI LIVE PAPER TRADING START
echo ======================================

echo Starting AI Trading Worker...
start "AI TRADING WORKER" cmd /k C:\Users\enes\ABD_Borsa_Robotu\venv\Scripts\python.exe -m runtime.trading_worker

timeout /t 2 > nul

echo Starting PNL Worker...
start "PNL WORKER" C:\Users\enes\ABD_Borsa_Robotu\venv\Scripts\python.exe -c "from runtime.pnl_worker import start_pnl_worker; start_pnl_worker(); print('PNL WORKER STARTED')"

timeout /t 2 > nul

echo Starting Dashboard...
start "DASHBOARD" C:\Users\enes\ABD_Borsa_Robotu\venv\Scripts\python.exe -m uvicorn app.web_dashboard_server:app --host 0.0.0.0 --port 8000

timeout /t 5 > nul

start http://localhost:8000

echo ======================================
echo ALL SYSTEMS STARTED
echo ======================================

pause
