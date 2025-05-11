import random
import string

def gen_email(domain='coderhack.net'):
    user = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{user}@{domain}"

# Quick test
if __name__ == "__main__":
    print(gen_email())