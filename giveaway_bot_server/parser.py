import re

def extract_verification_links(log_path="mail_log.txt"):
    """
    Reads the mail log and extracts unique Gleam verification links.
    """
    try:
        with open(log_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ mail_log.txt not found.")
        return []

    # Find all links that match Gleam format
    links = re.findall(r"https:\/\/gleam\.io\/[\w\-]+", content)
    return list(set(links))  # Deduplicate and return

def extract_links_from_latest_email(log_path="mail_log.txt"):
    """
    Grabs the latest block of email and extracts any Gleam links.
    """
    try:
        with open(log_path, "r") as f:
            blocks = f.read().split("="*60)
    except FileNotFoundError:
        print("❌ mail_log.txt not found.")
        return []

    if not blocks or len(blocks) < 2:
        return []

    latest_block = blocks[-2]  # Second to last block is the last full email
    links = re.findall(r"https:\/\/gleam\.io\/[\w\-]+", latest_block)
    return list(set(links))

# 🧪 Example Usage
if __name__ == "__main__":
    print("🔍 Extracting all Gleam links from log:")
    all_links = extract_verification_links()
    for link in all_links:
        print(f"🔗 {link}")

    print("\n🆕 Extracting from latest email:")
    new_links = extract_links_from_latest_email()
    for link in new_links:
        print(f"✨ {link}")