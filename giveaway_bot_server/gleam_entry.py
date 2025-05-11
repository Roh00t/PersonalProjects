import undetected_chromedriver.v2 as uc
from time import sleep
from emailgen import gen_email

def submit_email_to_gleam():
    email = gen_email()
    url = "https://gleam.io/UUrlm/spencers-ultimate-home-entertainment-giveaway"

    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")  # remove for debug visibility
    driver = uc.Chrome(options=options)

    try:
        driver.get(url)
        sleep(5)

        # Update these selectors as needed — based on Gleam’s current UI
        email_box = driver.find_element("css selector", "input[type='email']")
        email_box.send_keys(email)
        sleep(1)

        submit = driver.find_element("css selector", "button[type='submit']")
        submit.click()

        print(f"[+] Submitted: {email}")
        sleep(10)  # Allow time for verification trigger
    except Exception as e:
        print(f"[!] Gleam entry failed: {e}")
    finally:
        driver.quit()

    return email

# Run a test
if __name__ == "__main__":
    submit_email_to_gleam()