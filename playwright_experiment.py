from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.homechef.com/", wait_until="domcontentloaded")

    print("Page title:", page.title())
    print("Page URL:", page.url)

    input("Press Enter to close the browser...")

    browser.close()
