# -*- coding: UTF-8 -*-
import os, sys, time, base64, marshal, zlib
from datetime import datetime, timedelta

# Colors
green = "\033[0;32m"
yellow = "\033[0;33m"
cyan = "\033[0;36m"
white = "\033[0;37m"
red = "\033[0;31m"
ask = green + '\n[' + white + '?' + green + '] ' + yellow
success = green + '\n[' + white + '\u221a' + green + '] '
error = red + '\n[' + white + '!' + red + '] '
info = yellow + '\n[' + white + '+' + yellow + '] ' + cyan

logo = f"""{green}
██████╗ ██╗   ██╗███████╗ ██████╗ ██████╗ ██╗   ██╗███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██╔════╝ ██╔══██╗╚██╗ ██╔╝██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║  ███╗██████╔╝ ╚████╔╝ █████╗  
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██╔═══╝   ╚██╔╝  ██╔══╝  
██║        ██║   ███████╗╚██████╔╝██║        ██║   ███████╗
╚═╝        ╚═╝   ╚══════╝ ╚═════╝ ╚═╝        ╚═╝   ╚══════╝
              [🔐 LICENSE + COMBO OUTCOME9K]
"""

emoji_alphabet = [
    "😀", "😃", "😄", "😁", "😅", "🤣", "😂", "😉", "😊", "😛"
]

def sprint(text, sec=0.01):
    for char in text + '\n':
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(sec)

def generate_expiry_date():
    print(info + "Choose expiry time (can leave blank for 0):")
    mins = input(ask + "Minutes: ").strip()
    hrs = input(ask + "Hours: ").strip()
    days = input(ask + "Days: ").strip()
    months = input(ask + "Months: ").strip()
    years = input(ask + "Years: ").strip()
    try:
        total_days = int(days or 0) + int(months or 0) * 30 + int(years or 0) * 365
        delta = timedelta(
            minutes=int(mins or 0),
            hours=int(hrs or 0),
            days=total_days
        )
        expiry_time = datetime.now() + delta
        return expiry_time.strftime("%Y-%m-%d %H:%M:%S")
    except:
        print(error + "Invalid time input.")
        sys.exit(1)

def license_check_block(key, expiry):
    return f'''
import os, sys
from datetime import datetime
LICENSE_KEY = "{key}"
EXPIRY = "{expiry}"
def check():
    input_key = input("Enter License Key: ").strip()
    if input_key != LICENSE_KEY:
        print("\\033[91m[!] Invalid License Key!\\033[0m")
        try: os.remove(__file__)
        except: pass
        sys.exit(1)
    if datetime.now() > datetime.strptime(EXPIRY, "%Y-%m-%d %H:%M:%S"):
        print("\\033[91m[!] License expired!\\033[0m")
        try: os.remove(__file__)
        except: pass
        sys.exit(1)
check()
'''

def combo_obfuscate(code):
    # Step 1: Marshal+zlib+base64 encode
    encoded = base64.b64encode(zlib.compress(marshal.dumps(compile(code, "<combo>", "exec")))).decode()
    payload = f"""
import marshal, zlib, base64
exec(marshal.loads(zlib.decompress(base64.b64decode('{encoded}'))))
"""
    # Step 2: Emoji obfuscate
    d1 = dict(enumerate(emoji_alphabet))
    d2 = {v: k for k, v in d1.items()}
    obf = "  ".join(" ".join(d1[int(i)] for i in str(ord(c))) for c in payload)
    d2_str = repr(d2)
    emoji_encoded = (
        "d2 = " + d2_str + "\n" +
        f"obf = '''{obf}'''\n" +
        "exec(''.join(map(chr, [int(''.join(str(d2[i]) for i in x.split())) for x in obf.split('  ')])))"
    )
    return emoji_encoded

def admin_mode():
    print(green + "\n[Admin Mode - Combo Obfuscation with License]\n")
    source = input(ask + "Source Python file to protect: ").strip()
    if not os.path.isfile(source):
        print(error + "File not found.")
        return
    output = input(ask + "Output filename (.py): ").strip()
    if not output:
        print(error + "No output filename.")
        return
    key = input(ask + "License Key: ").strip()
    expiry = generate_expiry_date()
    with open(source, "r", encoding="utf-8") as f:
        original_code = f.read()
    combo_code = license_check_block(key, expiry) + "\n" + original_code
    final_code = combo_obfuscate(combo_code)
    with open(output, "w", encoding="utf-8") as out_f:
        out_f.write("# Combo Obfuscated with License Check\n" + final_code)
    print(success + f"✅ Output file: {output}")
    print(success + f"🔑 License Key: {key}")
    print(success + f"⏰ Expiry: {expiry}")

def main():
    os.system("clear")
    sprint(logo, 0.005)
    print(f"{green}[1]{yellow} Admin Mode (Combo + License)")
    print(f"{green}[0]{yellow} Exit")
    ch = input(ask + "Choose: ").strip()
    if ch == "1":
        admin_mode()
    else:
        print(info + "Goodbye.")
        sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + info + "Exited.")
