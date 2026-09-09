<div dir="rtl">

<div align="center">

<img src="assets/freemodels-proxy-logo.png" alt="FreeModels Proxy" width="150" />

# FreeModels Proxy

**یک پل محلی و سازگار با OpenAI بین FreeModels Chat و Cherry Studio — با پشتیبانی از Streaming و MCP / Tool Call.**

FreeModels Proxy روی ویندوز اجرا می‌شود و یک API محلی در اختیار Cherry Studio قرار می‌دهد تا Cherry Studio بتواند از طریق یک Base URL ساده به سرویس FreeModels متصل شود.

[![Release](https://img.shields.io/github/v/release/rkfcode/FreeModels-Proxy?display_name=tag&sort=semver)](https://github.com/rkfcode/FreeModels-Proxy/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/rkfcode/FreeModels-Proxy/total)](https://github.com/rkfcode/FreeModels-Proxy/releases)
[![License: MIT](https://img.shields.io/github/license/rkfcode/FreeModels-Proxy)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Platform](https://img.shields.io/badge/Windows-10%20%7C%2011-0078D6?logo=windows&logoColor=white)](#نیازمندیها)

**[English](README.md)** · فارسی

### [⬇️ دانلود FreeModels Proxy](https://github.com/rkfcode/FreeModels-Proxy/releases/latest)

**نسخه Release به‌صورت فایل اجرایی مستقل ویندوز ارائه می‌شود و برای اجرای آن نیازی به Python، pip، PowerShell یا نصب دستی وابستگی‌ها ندارید.**

</div>

---

## فهرست مطالب

- [چرا این پروژه ساخته شده است؟](#چرا-این-پروژه-ساخته-شده-است)
- [امکانات](#امکانات)
- [دانلود](#دانلود)
- [نصب و اجرا](#نصب-و-اجرا)
- [شروع سریع](#شروع-سریع)
- [اتصال به Cherry Studio](#اتصال-به-cherry-studio)
- [API](#api)
- [MCP و Tool Call](#mcp-و-tool-call)
- [پیکربندی](#پیکربندی)
- [تست](#تست)
- [حریم خصوصی و امنیت](#حریم-خصوصی-و-امنیت)
- [نیازمندی‌ها](#نیازمندیها)
- [ساخت از سورس](#ساخت-از-سورس)
- [ساختار پروژه](#ساختار-پروژه)
- [مستندات](#مستندات)
- [رفع مشکلات](#رفع-مشکلات)
- [مشارکت](#مشارکت)
- [مجوز](#مجوز)
- [توسعه‌دهنده و حمایت](#توسعهدهنده-و-حمایت)

---

## چرا این پروژه ساخته شده است؟

Cherry Studio برای کار با APIهای سازگار با OpenAI طراحی شده است، در حالی که FreeModels Chat سرویس Upstream مخصوص خود را دارد.

FreeModels Proxy این دو محیط را به هم متصل می‌کند:

```text
Cherry Studio
     │
     │ OpenAI-compatible API
     ▼
┌─────────────────────────┐
│    FreeModels Proxy     │
│       127.0.0.1:8000    │
│                         │
│  • سازگاری API          │
│  • Streaming            │
│  • پل Tool / MCP        │
│  • نرمال‌سازی درخواست   │
└────────────┬────────────┘
             │
             ▼
     FreeModels Chat
```

هدف پروژه ساده است:

**Cherry Studio همچنان محیط اصلی Client و Agent باقی بماند و FreeModels Proxy فقط لایه سازگاری بین Cherry Studio و سرویس FreeModels باشد.**

---

## امکانات

| | |
|---|---|
| 🪟 **لانچر دسکتاپ ویندوز** | رابط گرافیکی برای Start، Stop، Restart و مشاهده وضعیت Proxy. |
| 🚀 **شروع خودکار** | لانچر می‌تواند هنگام باز شدن برنامه Proxy را به‌صورت خودکار اجرا کند. |
| 🔌 **API سازگار با OpenAI** | API محلی با ساختار مناسب برای کلاینت‌های OpenAI-compatible. |
| 🤖 **آماده برای Cherry Studio** | Base URL پیشنهادی: `http://127.0.0.1:8000/v1` |
| 🌊 **پشتیبانی از Streaming** | پاسخ‌های Streaming با Server-Sent Events پشتیبانی می‌شوند. |
| 🧰 **پل MCP / Tool Call** | تعریف ابزارهای ارسال‌شده از Cherry Studio دریافت و Tool Callهای مدل به ساختار OpenAI تبدیل می‌شوند. |
| 🔄 **حفظ تاریخچه Tool Call** | پیام‌های assistant دارای Tool Call و نتایج ابزار برای ادامه چرخه Agent حفظ می‌شوند. |
| 🧠 **Model Routing** | درخواست‌ها با شناسه مدل انتخاب‌شده توسط Proxy پردازش و به Upstream ارسال می‌شوند. |
| 📋 **کپی سریع Base URL** | Base URL موردنیاز Cherry Studio مستقیماً از لانچر قابل کپی است. |
| 🧪 **دسترسی سریع به Test / Docs** | از داخل لانچر می‌توانید مستندات API و تست سرویس را باز کنید. |
| 📊 **اطلاعات Runtime** | Host، Port، وضعیت اجرا و اطلاعات اتصال در لانچر نمایش داده می‌شود. |
| 📝 **Live Logs** | فعالیت Proxy و اطلاعات درخواست‌ها در زمان اجرا قابل مشاهده است. |
| 🌐 **Host و Port قابل تنظیم** | بدون تغییر کد می‌توانید Host و Port سرویس را تغییر دهید. |
| 🌍 **رابط فارسی و انگلیسی** | لانچر از دو زبان فارسی و انگلیسی پشتیبانی می‌کند. |
| 📦 **فایل EXE مستقل** | نسخه Release با PyInstaller به فایل اجرایی ویندوز تبدیل می‌شود. |
| 🎨 **رابط کاربری مدرن** | لانچر با طراحی تیره و برندینگ اختصاصی FreeModels Proxy ساخته شده است. |
| 🔒 **Local-first** | به‌صورت پیش‌فرض API روی `127.0.0.1:8000` اجرا می‌شود. |

---

## دانلود

### پیشنهاد اصلی — نسخه ویندوز

به صفحه آخرین Release بروید:

**[⬇️ دانلود آخرین نسخه FreeModels Proxy](https://github.com/rkfcode/FreeModels-Proxy/releases/latest)**

برای کاربران عادی فایل زیر را دانلود کنید:

```text
FreeModels Proxy.exe
```

سپس فایل را اجرا کنید.

در نسخه Release نیازی نیست Python یا وابستگی‌های پروژه را به‌صورت دستی نصب کنید.

### نسخه سورس

اگر توسعه‌دهنده هستید و می‌خواهید کد را بررسی یا تغییر دهید، می‌توانید Repository را Clone کرده و نسخه Source را اجرا کنید.

---

## نصب و اجرا

### نسخه Release

1. وارد [آخرین Release در GitHub](https://github.com/rkfcode/FreeModels-Proxy/releases/latest) شوید.
2. فایل `FreeModels Proxy.exe` را دانلود کنید.
3. فایل را اجرا کنید.
4. لانچر Proxy را به‌صورت خودکار اجرا می‌کند.
5. Base URL نمایش‌داده‌شده را در Cherry Studio وارد کنید.

Base URL پیش‌فرض:

```text
http://127.0.0.1:8000/v1
```

### نکته مهم

برای کاربران عادی، استفاده از فایل EXE بهترین گزینه است.

نسخه Source برای توسعه‌دهندگان و افرادی است که قصد تغییر پروژه را دارند.

---

## شروع سریع

بعد از باز شدن لانچر:

1. مطمئن شوید وضعیت Proxy روی **Running** است.
2. Host را روی `127.0.0.1` و Port را روی `8000` بررسی کنید.
3. Base URL زیر را کپی کنید:

```text
http://127.0.0.1:8000/v1
```

4. Cherry Studio را باز کنید.
5. یک Provider از نوع OpenAI-compatible بسازید یا Provider فعلی را ویرایش کنید.
6. Base URL بالا را وارد کنید.
7. یکی از مدل‌های ارائه‌شده توسط Proxy را انتخاب کنید.
8. یک پیام آزمایشی ارسال کنید.

مستندات API نیز از آدرس زیر قابل دسترسی است:

```text
http://127.0.0.1:8000/docs
```

---

## اتصال به Cherry Studio

پیکربندی اولیه پیشنهادی:

| تنظیم | مقدار |
|---|---|
| نوع Provider | OpenAI-compatible |
| Base URL | `http://127.0.0.1:8000/v1` |
| API Key | خود Proxy برای اتصال محلی به API Key نیاز ندارد |
| Model | یکی از مدل‌های ارائه‌شده توسط `/v1/models` |

### چرا `/v1`؟

Endpoint اصلی Chat در Proxy این است:

```text
POST /v1/chat/completions
```

بنابراین در Cherry Studio باید Base URL زیر را وارد کنید:

```text
http://127.0.0.1:8000/v1
```

و نباید `/chat/completions` را به‌صورت دستی به انتهای Base URL اضافه کنید.

---

## API

### دریافت لیست مدل‌ها

```http
GET /v1/models
```

### دریافت یک مدل

```http
GET /v1/models/{model_id}
```

### Chat Completions

```http
POST /v1/chat/completions
```

این Endpoint از پاسخ‌های Streaming با Server-Sent Events پشتیبانی می‌کند.

### مسیر سازگاری بدون `/v1`

```http
POST /chat/completions
```

این مسیر برای کلاینت‌هایی در نظر گرفته شده که از Prefix `/v1` استفاده نمی‌کنند.

### مستندات تعاملی FastAPI

```text
http://127.0.0.1:8000/docs
```

---

## MCP و Tool Call

یکی از دلایل اصلی ساخت این Proxy، حفظ قابلیت‌های Agent و Tool در Cherry Studio است؛ نه اینکه ارتباط فقط به یک چت متنی ساده تبدیل شود.

Proxy می‌تواند:

1. Toolهای ارسال‌شده توسط Cherry Studio را دریافت کند.
2. نام ابزارهای MCP را برای قالب مورد انتظار مدل Map کند.
3. Tool Callهای متنی تولیدشده توسط مدل را تشخیص دهد.
4. آن‌ها را دوباره به ساختار OpenAI-compatible `tool_calls` تبدیل کند.
5. پیام‌های Tool Call و Tool Result را برای Turnهای بعدی حفظ کند.
6. پاسخ را به‌صورت Streaming به Cherry Studio برگرداند.

نمای کلی:

```text
Cherry Studio
    │
    │ tools + messages
    ▼
FreeModels Proxy
    │
    ├── نرمال‌سازی پیام‌ها
    ├── Map کردن نام ابزارهای MCP
    ├── تبدیل Tool به قالب قابل فهم برای مدل
    ├── تشخیص Tool Call برگشتی
    └── تبدیل به OpenAI tool_calls
    │
    ▼
Cherry Studio Agent
    │
    └── اجرای واقعی MCP Tool
```

**اجرای واقعی ابزار همچنان توسط Cherry Studio انجام می‌شود.**

FreeModels Proxy نقش لایه سازگاری و تبدیل بین Client و سرویس مدل را دارد.

---

## پیکربندی

### Listener پیش‌فرض

```text
Host: 127.0.0.1
Port: 8000
Base URL: http://127.0.0.1:8000/v1
```

برای اجرای مستقیم نسخه Python، متغیرهای محیطی زیر نیز قابل استفاده هستند:

```text
FREEMODELS_HOST
FREEMODELS_PORT
```

مثال:

```powershell
$env:FREEMODELS_HOST="127.0.0.1"
$env:FREEMODELS_PORT="8001"
python main.py
```

### امکانات قابل کنترل از لانچر

- Host
- Port
- Start / Stop
- Restart
- Auto Start
- Base URL
- API Docs / Test
- زبان رابط
- Runtime information
- Live logs

---

## تست

### تست از مرورگر

بعد از اجرای Proxy آدرس زیر را باز کنید:

```text
http://127.0.0.1:8000/docs
```

اگر مستندات FastAPI نمایش داده شد، سرویس محلی در حال اجراست.

### تست مدل‌ها

آدرس زیر را باز کنید:

```text
http://127.0.0.1:8000/v1/models
```

باید یک لیست مدل با ساختار OpenAI دریافت کنید.

### تست Cherry Studio

Base URL زیر را تنظیم کنید:

```text
http://127.0.0.1:8000/v1
```

سپس یک پیام کوتاه ارسال کنید.

### تست MCP / Tool

برای تست Agent، در Cherry Studio یک Workflow داشته باشید که حداقل یک MCP Tool در اختیار مدل قرار دهد.

Proxy باید Tool definitionها را دریافت کند، Tool Call مدل را به ساختار OpenAI برگرداند و اجازه دهد Cherry Studio چرخه اجرای Tool را ادامه دهد.

---

## حریم خصوصی و امنیت

FreeModels Proxy با رویکرد **Local-first** طراحی شده است.

- API محلی به‌صورت پیش‌فرض روی `127.0.0.1` اجرا می‌شود.
- درخواست Cherry Studio ابتدا به Proxy محلی می‌رسد.
- Proxy اطلاعات موردنیاز درخواست را به سرویس Upstream مربوط به FreeModels ارسال می‌کند.
- Proxy برای اجرای عادی به دیتابیس یا سیستم حساب کاربری محلی جداگانه نیاز ندارد.
- اگر Host را از `127.0.0.1` به یک آدرس دیگر تغییر دهید، ممکن است API از طریق شبکه برای سیستم‌های دیگر قابل دسترسی شود.

### نکته امنیتی

این پروژه یک Compatibility Proxy است، نه یک Security Boundary.

اگر سرویس را خارج از localhost در دسترس قرار می‌دهید، قبل از استفاده روی شبکه غیرقابل اعتماد، کنترل‌های مناسب شبکه و فایروال را در نظر بگیرید.

---

## نیازمندی‌ها

### برای کاربران عادی

هدف نسخه دسکتاپ، **Windows 10 و Windows 11** است.

در نسخه Standalone:

- Python لازم نیست.
- pip لازم نیست.
- PowerShell لازم نیست.
- FastAPI / httpx / uvicorn نیاز به نصب دستی ندارند.

### برای توسعه از سورس

به موارد زیر نیاز دارید:

- Windows
- Python 3.x
- pip
- پکیج‌های موجود در `requirements.txt`

---

## ساخت از سورس

Repository را Clone کنید:

```powershell
git clone https://github.com/rkfcode/FreeModels-Proxy.git
cd FreeModels-Proxy
```

محیط مجازی را بسازید:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

لانچر را اجرا کنید:

```powershell
.venv\Scripts\pythonw.exe launcher.py
```

### ساخت فایل EXE

در پروژه فایل زیر وجود دارد:

```text
build_windows.bat
```

اجرا:

```powershell
.\build_windows.bat
```

فایل نهایی در مسیر زیر ساخته می‌شود:

```text
dist\FreeModels Proxy.exe
```

ساخت Release با PyInstaller انجام می‌شود و Assetهای برنامه و وابستگی‌های Python نیز در بسته قرار می‌گیرند.

---

## ساختار پروژه

```text
FreeModels-Proxy/
├── launcher.py
├── main.py
├── requirements.txt
├── FreeModels Proxy.bat
├── build_windows.bat
├── README.md
├── README.fa.md
├── .gitignore
└── assets/
    ├── freemodels-proxy-logo.png
    └── freemodels-proxy.ico
```

### وظیفه فایل‌ها

| فایل | کاربرد |
|---|---|
| `main.py` | FastAPI Proxy، نرمال‌سازی درخواست، Model Routing، Streaming و Tool Call |
| `launcher.py` | لانچر دسکتاپ ویندوز و کنترل Runtime |
| `requirements.txt` | وابستگی‌های Python برای نسخه Source |
| `FreeModels Proxy.bat` | اجرای نسخه Source |
| `build_windows.bat` | ساخت نسخه Release با PyInstaller |
| `assets/` | لوگو و آیکون ویندوز برنامه |

---

## مستندات

در نسخه فعلی، مستندات اصلی پروژه در READMEهای انگلیسی و فارسی و مستندات خود FastAPI قرار دارند.

| منبع | کاربرد |
|---|---|
| [README انگلیسی](README.md) | معرفی و راه‌اندازی پروژه |
| [README فارسی](README.fa.md) | راهنمای فارسی |
| `http://127.0.0.1:8000/docs` | مستندات تعاملی FastAPI |
| `/v1/models` | Endpoint دریافت مدل‌ها |
| `/v1/chat/completions` | Endpoint اصلی Chat |

با توسعه پروژه می‌توان در آینده پوشه `docs/` را برای راهنمای نصب، استفاده، معماری، رفع خطا و انتشار اضافه کرد، بدون اینکه ساختار اصلی README تغییر کند.

---

## رفع مشکلات

| مشکل | چه چیزی را بررسی کنیم؟ |
|---|---|
| Cherry Studio وصل نمی‌شود | بررسی کنید Proxy در حال اجرا باشد و Base URL روی `http://127.0.0.1:8000/v1` باشد. |
| `/docs` باز نمی‌شود | وضعیت Proxy، Host و Port را در لانچر بررسی کنید. |
| `/v1/models` در دسترس نیست | Live Logs و اتصال به Upstream را بررسی کنید. |
| درخواست یک مدل خطا می‌دهد | Model ID انتخاب‌شده و Logهای Proxy را بررسی کنید. |
| Agent / Tool متوقف می‌شود | بررسی کنید Cherry Studio واقعاً `tools` را ارسال می‌کند و مدل انتخاب‌شده برای Workflow مناسب است. |
| Port 8000 اشغال است | Port را در لانچر تغییر دهید و سپس Base URL جدید را در Cherry Studio قرار دهید. |
| EXE اجرا نمی‌شود | آخرین Release را امتحان کنید و بررسی کنید Windows Security یا Antivirus فایل را مسدود نکرده باشد. |
| نسخه Source اجرا نمی‌شود | `.venv` را دوباره بسازید و `requirements.txt` را مجدداً نصب کنید. |

برای عیب‌یابی، ابتدا Live Logs داخل لانچر را بررسی کنید.

---

## مشارکت

برای Issue، پیشنهاد و Pull Request خوشحال می‌شویم.

قبل از ارسال تغییرات:

1. ساختار و سبک فعلی پروژه را حفظ کنید.
2. در منطق سازگاری Request/Response تغییرات غیرضروری ایجاد نکنید.
3. اگر Message Handling را تغییر می‌دهید، هم Chat معمولی و هم MCP / Tool Workflow را تست کنید.
4. README را با رفتار واقعی پروژه هماهنگ نگه دارید.
5. هیچ Token، Credential یا Secret محلی را Commit نکنید.

---

## مجوز

این پروژه تحت **MIT License** منتشر شده است.

متن کامل مجوز در فایل [LICENSE](LICENSE) قرار دارد.

پکیج‌های Third-party مجوزهای مخصوص خود را دارند.

---

## توسعه‌دهنده و حمایت

ساخته‌شده توسط **Reza Kazemi**.

[![GitHub](https://img.shields.io/badge/GitHub-rkfcode-181717?logo=github)](https://github.com/rkfcode)

Repository:

**[github.com/rkfcode/FreeModels-Proxy](https://github.com/rkfcode/FreeModels-Proxy)**

اگر این پروژه برایتان مفید بود، یک ⭐ در GitHub واقعاً به دیده‌شدن و ادامه توسعه پروژه کمک می‌کند.

### حمایت از پروژه

- [Daramet — حمایت ریالی](https://daramet.com/RKFi)
- [Donatr.ee — USD / Crypto](https://donatr.ee/rkfcode/)

<div align="center">

**FreeModels Proxy**  
*لایه سازگاری محلی بین FreeModels Chat و Cherry Studio*

</div>

</div>
