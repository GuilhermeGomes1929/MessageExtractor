from playwright.sync_api import sync_playwright
import time

FIREFOX_PATH = 'C:\Program Files\Mozilla Firefox'

with sync_playwright() as p:
    browser = p.firefox.launch_persistent_context(FIREFOX_PATH, headless=False)
    page = browser.new_page()
    page.goto("https://web.whatsapp.com/")
    input("Log no Whatsapp, entre na conversa e pressione qualquer tecla")
    
    time.sleep(2)
    for i in range(4):
        page.evaluate(
            """
                mainContainer = document.querySelector('#main > div._2gzeB > div > div._33LGR')
                mainContainer.scrollBy(0, -350)
            """
        )
        time.sleep(2)
    print(page.title())
    browser.close()