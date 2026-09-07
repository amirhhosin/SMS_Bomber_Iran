# ☠️ SMS BOMBER v3.0 - HACKER EDITION

<div align="center">
  <img src="https://img.shields.io/badge/Version-3.0-red?style=for-the-badge&logo=github" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.10+-green?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Termux-red?style=for-the-badge&logo=android" alt="Platform">
  <img src="https://img.shields.io/badge/License-Educational-purple?style=for-the-badge" alt="License">
</div>

---

## ☠️ About

**SMS BOMBER v3.0** یک ابزار برای ارسال درخواست OTP به ۸۰+ سرویس مختلف به صورت همزمان است. دارای تم گرافیکی، قابلیت مولتی‌ترد، پشتیبانی از پروکسی و **رابط کاربری وب**.

### 🔥 Features

| ویژگی | توضیح |
| :--- | :--- |
| 💀 **۸۰+ سرویس** | پشتیبانی از اکثر سرویس‌های محبوب |
| 🔥 **مولتی‌ترد** | تنظیم ۱ تا ۳۰ ترد همزمان |
| 🩸 **پروکسی** | استفاده از پروکسی‌های فایل `proxies.txt` |
| 📱 **چند شماره** | پشتیبانی از ۳ شماره همزمان |
| 🎯 **تم جذاب** | طراحی مدرن و حرفه‌ای |
| 🌐 **رابط کاربری وب** | اجرا از طریق مرورگر با Flask |
| 💻 **خط فرمان** | اجرا مستقیم از ترمینال |

---

## 📦 Installation

### Termux (Android)

```bash
# Clone repository
git clone https://github.com/amirhhosin/SMS_Bomber_Iran.git
cd SMS_Bomber_Iran

# Run installer
bash setup.sh

# Start tool
python main.py
```

---

## 🚀 How to Use

### 1️⃣ Terminal Mode (CLI)

```bash
python main.py 09123456789 3 15
```

| پارامتر | توضیح |
| :--- | :--- |
| `09123456789` | شماره هدف |
| `3` | تعداد درخواست (۱ تا ۵۰) |
| `15` | تعداد ترد (۱ تا ۳۰) |

### 2️⃣ Web Mode (UI)

```bash
python app.py
```

سپس در مرورگر آدرس زیر را باز کنید:

```text
http://127.0.0.1:5000
```

### 3️⃣ Interactive Mode

```bash
python main.py
```

و طبق راهنمایی برنامه پیش بروید.

---

## 🖥️ Web Interface Screenshot

```text
┌────────────────────────────────────────────────────────────┐
│  ☠️ SMS BOMBER                                            │
│  HACKER EDITION v3.0 — by amirhhosin                     │
│  🔴 READY FOR ATTACK                                     │
├────────────────────────────────────────────────────────────┤
│  📱 شماره هدف: 09123456789                                │
│  ⚡ تعداد اسپم: 3                                        │
│  🧵 تعداد ترد: 15                                       │
│  [🔥 اجرای حمله]                                         │
├────────────────────────────────────────────────────────────┤
│  ATTACK LOG — amirhhosin                                 │
│  ●  ●  ●                                                 │
│  ✅ عملیات با موفقیت انجام شد!                           │
└────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```text
SMS_Bomber_Iran/
├── main.py            # اسکریپت اصلی (CLI)
├── app.py             # سرور Flask (Web UI)
├── templates/
│   └── index.html     # رابط کاربری وب
├── static/
│   ├── logo.png       # لوگو
│   └── click.mp3      # صدای کلیک
├── requirements.txt   # کتابخانه‌های مورد نیاز
├── setup.sh           # نصب‌کننده خودکار
├── proxies.txt        # لیست پروکسی (اختیاری)
├── README.md          # راهنمای پروژه
└── .gitignore
```

---

## 📦 Requirements

```text
flask>=2.0.0
requests>=2.31.0
colorama>=0.4.6
fake-useragent>=1.4.0
urllib3>=2.0.0
```

### Termux Packages

```bash
pkg install python termux-speaker termux-media-player sox
```

---

## ⚠️ Disclaimer

<div align="center">
  <b>
    <p style="color:red;">
      ☠️ THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY ☠️
    </p>
    <p>
      Any improper or illegal use is the responsibility of the individual.
    </p>
    <p>
      The developer is not responsible for any misuse of this tool.
    </p>
  </b>
</div>

---

## 📞 Contact

* **Telegram:** [@amirhhosin](https://t.me/amirhhosin)
* **GitHub:** [amirhhosin](https://github.com/amirhhosin)

---

<div align="center">
  <img src="https://img.shields.io/badge/☠️-HACKER_EDITION-red?style=for-the-badge" alt="Hacker Edition">
  <img src="https://img.shields.io/badge/💀-ANONYMOUS-black?style=for-the-badge" alt="Anonymous">
  <img src="https://img.shields.io/badge/🔥-LEGION-green?style=for-the-badge" alt="Legion">
</div>

