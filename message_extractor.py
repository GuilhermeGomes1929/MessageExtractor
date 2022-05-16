from datetime import datetime
from playwright.sync_api import sync_playwright
import time
import re

def initAttributes(page):
    page.evaluate(
        """
        mainContainer = document.querySelector('#main > div._2gzeB > div > div._33LGR');
        messagesContainer = mainContainer.children[2];
        messagesHTML = messagesContainer.getElementsByClassName('_22Msk');
        firstMessageDate = messagesHTML[0].children[0].getAttribute('data-pre-plain-text');
        """
    )

def getFirstMessageDate(page):
    firstMessageDate = page.evaluate("() =>  messagesContainer.querySelector('._22Msk').querySelector('.copyable-text').getAttribute('data-pre-plain-text')")
    return firstMessageDate


def scrollUpToRefreshMessages(page):
    page.evaluate(
        """
        mainContainer.scrollBy(0, -800);
        """
    )
    time.sleep(1)
        
def getDateFromText(text):
    dateFormat = '%H:%M, %d/%m/%Y'
    regex = re.search(r"(\d{2}:\d{2}, \d{2}/\d{2}/\d{4})", text)
    dateString = regex.group()
    date = datetime.strptime(dateString, dateFormat)
    return date      

with sync_playwright() as p:
    DATE_FORMAT = "%d/%m/%Y %H:%M:%S"
    browser = p.chromium.launch_persistent_context(user_data_dir='', headless=False)
    page = browser.new_page()
    page.goto("https://web.whatsapp.com/")

    input("Faça o Login no Whatsapp, entre na conversa, espere sincronizar e pressione enter")
    time.sleep(1)
    initAttributes(page=page)
    limitDate = datetime.strptime("04/05/2022 00:00:00", DATE_FORMAT)
    print(f"Data Limite: {limitDate.strftime(DATE_FORMAT)}")
    while(True):
        scrollUpToRefreshMessages(page=page)
        dateStringFromMessageDate = getFirstMessageDate(page=page)
        date = getDateFromText(dateStringFromMessageDate)

        print(f"Data da última mensagem carregada: {date.strftime(DATE_FORMAT)}")    

        if (date < limitDate):
            print("Data da última mensagem é igual a data limite. Encerrando o processo!")
            break

    allHTML = page.content()
    extractedMessages = open('extractedMessages.txt')
    extractedMessages.write(allHTML)

    input()
    browser.close()
