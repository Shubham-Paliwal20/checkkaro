@echo off
SET PATH=C:\Program Files\Git\cmd;%PATH%
cd /d D:\knowyourproduct\checkkaro\mobile
echo Running flutter pub get... > D:\pub_get_log.txt 2>&1
flutter pub get >> D:\pub_get_log.txt 2>&1
echo Exit code: %ERRORLEVEL% >> D:\pub_get_log.txt 2>&1
echo DONE >> D:\pub_get_log.txt 2>&1
