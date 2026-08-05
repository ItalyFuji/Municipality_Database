@echo off
echo [1/5] Extracting municipality data from PDF...
python 01_extract_from_JapanMunicipalityPDF.py
if errorlevel 1 (
    echo ERROR: Step 1 failed.
    pause
    exit /b 1
)

echo [2/5] Removing exact duplicate rows...
python 02_remove_exact_duplicates.py
if errorlevel 1 (
    echo ERROR: Step 2 failed.
    pause
    exit /b 1
)

echo [3/5] Removing designated-city wards...
python 03_remove_wards.py
if errorlevel 1 (
    echo ERROR: Step 3 failed.
    pause
    exit /b 1
)

echo [4/5] Normalizing categories and short names...
python 04_normalize_municipality.py
if errorlevel 1 (
    echo ERROR: Step 4 failed.
    pause
    exit /b 1
)

echo [5/5] Removing same-prefecture name duplicates...
python 05_remove_name_duplicates.py
if errorlevel 1 (
    echo ERROR: Step 5 failed.
    pause
    exit /b 1
)

echo Done. Output: data_output/municipality_DB.csv
pause
