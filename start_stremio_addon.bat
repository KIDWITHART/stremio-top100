@echo off
title Stremio Top 100 TV Shows Addon Server
echo Starting Top 100 TV Shows Stremio Addon...
echo Manifest URL: http://localhost:7070/manifest.json
echo Stremio Install Link: stremio://localhost:7070/manifest.json
echo.
python stremio_addon.py
pause
