# main.py
# ساخته شده توسط OxSecTrack
# مدیر تونل‌های SSH ساده و امن

import argparse
from tunnel import create_ssh_tunnel

def main():
    parser = argparse.ArgumentParser(description="SSH Tunnel Manager by OxSecTrack")
    parser.add_argument('--host', required=True, help='آدرس سرور SSH (مثال: 192.168.1.10)')
    parser.add_argument('--user', required=True, help='نام کاربری SSH')
    parser.add_argument('--password', help='رمز عبور SSH (اختیاری اگر از کلید استفاده می‌کنید)')
    parser.add_argument('--port', type=int, default=22, help='پورت SSH (پیش‌فرض 22)')
    parser.add_argument('--local-port', type=int, required=True, help='پورت لوکال برای فوروارد')
    parser.add_argument('--remote-port', type=int, required=True, help='پورت مقصد در سرور')
    parser.add_argument('--key', help='مسیر فایل کلید خصوصی (اختیاری)')

    args = parser.parse_args()

    print("[OxSecTrack] شروع اتصال SSH به سرور...")
    create_ssh_tunnel(
        host=args.host,
        username=args.user,
        password=args.password,
        port=args.port,
        local_port=args.local_port,
        remote_port=args.remote_port,
        key_file=args.key
    )
    print("[OxSecTrack] عملیات تونل SSH کامل شد.")

if __name__ == "__main__":
    main()