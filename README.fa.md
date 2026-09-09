<p align="center">
  <img src="assets/freemodels-proxy-logo.png" alt="FreeModels Proxy" width="420">
</p>

<p align="center"><strong>پروکسی محلی سازگار با OpenAI برای Cherry Studio</strong></p>

# FreeModels Proxy

[English](README.md) | فارسی

یک لانچر دسکتاپ ویندوز با رابط کاربری برای اجرای پروکسی محلی سازگار با OpenAI.

## برای کاربران عادی

از بخش **GitHub Releases** فایل `FreeModels Proxy.exe` را دانلود کنید و فقط روی آن دوبار کلیک کنید.

نیازی به نصب موارد زیر نیست:

- Python
- pip
- PowerShell
- وابستگی‌های پروژه


## EXE مستقل

نسخه پیشنهادی برای کاربران نهایی `FreeModels Proxy.exe` است. این فایل Runtime و وابستگی‌های برنامه را همراه خود دارد، پروکسی را خودکار اجرا می‌کند و به نصب دستی Python، pip، PowerShell یا Dependency نیاز ندارد.

## نسخه سورس

برای اجرای سورس:

1. پروژه را دانلود و Extract کنید.
2. روی `FreeModels Proxy.bat` دوبار کلیک کنید.
3. اجرای اول به‌صورت خودکار یک محیط محلی `.venv` می‌سازد و وابستگی‌ها را نصب می‌کند.
4. اجراهای بعدی مستقیم برنامه را باز می‌کنند.

## توسعه‌دهنده

**Reza Kazemi**

GitHub: https://github.com/rkfcode

## حمایت مالی

- حمایت ریالی: https://daramet.com/RKFi
- حمایت دلاری و ارز دیجیتال: https://donatr.ee/rkfcode/

## ساخت EXE

روی ویندوز فایل `build_windows.bat` را اجرا کنید.

خروجی:

`dist/FreeModels Proxy.exe`

برای کاربران نهایی، فایل EXE را در GitHub Releases منتشر کنید.

## Cherry Studio

Base URL:

`http://127.0.0.1:8000/v1`
