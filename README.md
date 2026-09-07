# ☠️ SMS BOMBER v3.0 — HACKER EDITION

<div align="center">

<img src="https://img.shields.io/badge/Version-3.0-red?style=for-the-badge&logo=github" alt="Version">
<img src="https://img.shields.io/badge/Python-3.10+-green?style=for-the-badge&logo=python" alt="Python">
<img src="https://img.shields.io/badge/Platform-Termux-red?style=for-the-badge&logo=android" alt="Platform">
<img src="https://img.shields.io/badge/License-Educational-purple?style=for-the-badge" alt="License">

<br><br>

**Cyberpunk Web Interface & API Testing Demo**

</div>

---

## ☠️ About

**SMS BOMBER v3.0** یک پروژه آموزشی برای آشنایی با ساختار ابزارهای
تست API، رابط‌های وب و اجرای درخواست‌های آزمایشی در محیط محلی است.

این نسخه برای استفاده در **محیط تست و سرویس‌های تحت کنترل خودتان** طراحی شده
و هیچ پیام واقعی برای اشخاص یا سرویس‌های شخص ثالث ارسال نمی‌کند.

---

## 🔥 Features

| ویژگی | توضیح |
|---|---|
| 🖥️ **Web Interface** | رابط کاربری مدرن با Flask |
| 💻 **CLI** | اجرای پروژه از طریق ترمینال |
| 🧪 **API Testing** | شبیه‌سازی درخواست‌ها در محیط آزمایشی |
| 🧵 **Multi-Thread Demo** | نمایش مفهوم اجرای همزمان در محیط تست |
| 📱 **Mobile Friendly** | مناسب برای Termux و مرورگر موبایل |
| 🎨 **Cyberpunk UI** | رابط کاربری با تم Neon/Cyberpunk |
| 📊 **Console Logs** | نمایش وضعیت اجرای تست‌ها |

---

## 📦 Installation

### Termux

```bash
git clone https://github.com/amirhhosin/SMS_Bomber_Iran.git

cd SMS_Bomber_Iran

bash setup.sh
```

---

## 🚀 Usage

### 🖥️ Web Mode

اجرای رابط وب:

```bash
python app.py
```

سپس مرورگر را باز کنید:

```text
http://127.0.0.1:5000
```

### 💻 CLI Mode

برای اجرای محیط آزمایشی:

```bash
python main.py
```

> این پروژه در حالت Demo فقط درخواست‌های محلی/آزمایشی را شبیه‌سازی می‌کند.

---

## 🖥️ Web Interface

رابط وب پروژه با تمرکز روی طراحی Cyberpunk ساخته شده است.

```text
┌────────────────────────────────────────────────────────────┐
│                                                            │
│                 ☠️ CYBER CONSOLE                          │
│                                                            │
│              HACKER EDITION v3.0                           │
│                                                            │
│                 ● SYSTEM ONLINE                            │
│                                                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  📱 شماره آزمایشی: 09123456789                             │
│                                                            │
│  ⚡ تعداد درخواست: 3                                       │
│                                                            │
│  🧵 Worker Threads: 5                                     │
│                                                            │
│              [ ▶ اجرای تست ]                              │
│                                                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  TERMINAL OUTPUT                              ● LIVE       │
│                                                            │
│  > Initializing test environment...                        │
│  > Running local simulation...                             │
│  > Completed successfully.                                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```text
SMS_Bomber_Iran/
│
├── main.py
├── app.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── logo.png
│   └── click.mp3
│
├── requirements.txt
├── setup.sh
├── README.md
└── .gitignore
```

---

## 📦 Requirements

```txt
flask>=2.0.0
requests>=2.31.0
colorama>=0.4.6
urllib3>=2.0.0
```

### Termux Packages

```bash
pkg update

pkg install python

pkg install termux-media-player

pkg install sox
```

---

## 🧪 Testing

برای تست پروژه از شماره‌ها و سرویس‌های واقعی دیگران استفاده نکنید.

پیشنهاد می‌شود تست‌ها را با:

- API محلی
- Mock Server
- شماره‌های آزمایشی
- سرویس‌هایی که خودتان کنترل می‌کنید

انجام دهید.

---

## ⚠️ Disclaimer

> ☠️ **EDUCATIONAL PROJECT**
>
> این پروژه صرفاً برای آموزش مفاهیم Python، Flask، API Testing،
> Multi-threading و طراحی رابط کاربری ایجاد شده است.
>
> استفاده از این پروژه علیه اشخاص، شماره‌ها یا سرویس‌هایی که
> مالک آن نیستید مجاز نیست.
>
> مسئولیت استفاده از پروژه بر عهده کاربر است.

---

## 👨‍💻 Author

**amirhhosin**

- GitHub: `amirhhosin`
- Telegram: `@amirhhosin`

---

## 📜 License

این پروژه با هدف آموزشی و آزمایشی منتشر شده است.

---

<div align="center">

<img src="https://img.shields.io/badge/☠️-HACKER_EDITION-red?style=for-the-badge" alt="Hacker Edition">
<img src="https://img.shields.io/badge/💀-CYBER_CONSOLE-black?style=for-the-badge" alt="Cyber Console">
<img src="https://img.shields.io/badge/🔥-EDUCATIONAL-green?style=for-the-badge" alt="Educational">

<br><br>

**Built for learning. Designed for experimentation.**

</div>

