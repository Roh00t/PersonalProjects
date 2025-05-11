import smtpd
import asyncore

class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print(f"\n📨 Incoming mail from: {mailfrom}")
        print(f"📥 To: {rcpttos}")
        print("📄 Data:")
        print(data)
        print("="*70)

        # ✅ Save to mail_log.txt for later parsing
        with open("mail_log.txt", "a") as f:
            f.write(f"From: {mailfrom}\nTo: {rcpttos}\n{data}\n")
            f.write("="*60 + "\n")

    def handle_RCPT(self, command, arg):
        address = arg.split(":")[-1].strip("<>")
        if not address.endswith("@coderhack.net"):
            return '550 Invalid recipient'
        return super().handle_RCPT(command, arg)

if __name__ == "__main__":
    bind_ip = "0.0.0.0"  # Use your private IP (e.g., 192.168.x.x) if 0.0.0.0 fails
    port = 25

    print(f"🚀 Starting SMTP server for coderhack.net on {bind_ip}:{port}...")
    server = CustomSMTPServer((bind_ip, port), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user.")