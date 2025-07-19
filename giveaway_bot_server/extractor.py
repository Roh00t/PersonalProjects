import re

def extract_verification_links(log_path="mail_log.txt"):
    with open(log_path, "r") as f:
        content = f.read()
    links = re.findall(r"https:\/\/gleam\.io\/[\w\-]+", content)
    return list(set(links))  # Deduplicate links

# Example usage
if __name__ == "__main__":
    links = extract_verification_links()
    for link in links:
        print(f"🔗 Found: {link}")