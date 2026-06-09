@echo off
title Demarrage - Moroccan Coins Detection
echo ===================================================================
echo   Moroccan Coins Detection and Total Amount Calculation
echo ===================================================================
echo.
echo Verification de l'installation de Streamlit...
streamlit --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Streamlit n'est pas installe ou n'est pas dans votre PATH.
    echo.
    echo Veuillez executer la commande suivante dans votre terminal :
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b
)

echo [INFO] Démarrage du serveur Streamlit local...
echo [INFO] L'application va s'ouvrir automatiquement dans votre navigateur.
echo.
streamlit run app/app.py
pause
