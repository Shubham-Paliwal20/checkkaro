@echo off
REM Run this from File Explorer (double-click) to build release APKs
REM Output: build\app\outputs\flutter-apk\app-arm64-v8a-release.apk

git config --global --add safe.directory C:/flutter 2>nul

SET PATH=C:\Program Files\Git\cmd;C:\flutter\bin;C:\Program Files\Eclipse Adoptium\jdk-17.0.19.10-hotspot\bin;C:\Windows\System32;C:\Windows;C:\Users\Hp\AppData\Local\Android\sdk\platform-tools

cd /d D:\knowyourproduct\checkkaro\mobile

echo Building release APKs...
"C:\flutter\bin\cache\dart-sdk\bin\dart.exe" --disable-dart-dev --packages="C:\flutter\packages\flutter_tools\.dart_tool\package_config.json" "C:\flutter\bin\cache\flutter_tools.snapshot" build apk --release --split-per-abi

echo.
echo APKs are in: build\app\outputs\flutter-apk\
echo Share app-arm64-v8a-release.apk for modern phones.
pause
