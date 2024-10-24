import re
from playwright.sync_api import Page
from time import sleep
import validators

def test_example(page: Page) -> None:
    email = "meshareef19@gmail.com"
    password = ".-n76b*U8^vMRn_"
    company = "Deutsche Bahn"
    location = "Frankfurt Rhine-Main Metropolitan Area"
    jobTile = "HR"
    messageCount = 0
    connectCount = 0
    followCount = 0
    pendingCount = 0
    linkedInMemberCount = 0
    connectLinkList = []
    # location = input("Enter the location(exactly how on the web site): ")
    # jobTile = input("Enter the job title: ")
    # company = input("Enter the company name: ")
    page.goto("https://www.linkedin.com/")
    page.locator("[data-test-id=\"home-hero-sign-in-cta\"]").click()
    page.get_by_label("Email or phone").fill(email)
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill(password)
    page.get_by_label("Sign in", exact=True).click()
    page.get_by_placeholder("Search", exact=True).click()
    page.get_by_placeholder("Search", exact=True).fill(company)
    page.get_by_placeholder("Search", exact=True).press("Enter")
    page.get_by_role("button", name="People").click()
    page.get_by_label("Locations filter. Clicking").click()
    page.get_by_label("Show all filters. Clicking").click()
    page.get_by_label("Title").click()
    page.get_by_label("Title").fill(jobTile)
    page.get_by_text(company, exact=True).first.click()
    page.get_by_role("button", name="Add a location").click()
    page.get_by_role("combobox", name="Add a location").fill(location)
    sleep(2)
    page.get_by_role("combobox", name="Add a location").press("ArrowDown")
    page.get_by_role("combobox", name="Add a location").press("Enter")
    page.get_by_label("Apply current filters to show").click()
    results_text = page.locator("div:not([class]):not([id])", has_text=re.compile(r"\d+ results")).inner_text()
    results_number = int(re.search(r'\d+', results_text).group())
    numberOfPages = results_number // 10
    remainder = results_number % 10
    page.keyboard.press("Tab")
    for a in range(numberOfPages):
        for b in range(10):
            page.keyboard.press("Tab")
            sleep(0.4)
            name = page.evaluate("document.activeElement.innerText")
            if name == "LinkedIn Member":
                linkedInMemberCount += 1
                continue
            link = page.evaluate("document.activeElement.href")
            page.keyboard.press("Tab")
            sleep(0.4)
            button_text = page.evaluate("document.activeElement.innerText")
            if button_text not in ["Message", "Connect", "Follow", "Pending"]:
                page.keyboard.press("Tab")
                sleep(0.4)
                button_text = page.evaluate("document.activeElement.innerText")
            if button_text == "":
                page.keyboard.press("Tab")
                sleep(0.4)
                button_text = page.evaluate("document.activeElement.innerText")
            if button_text == "Message":
                messageCount += 1
                connectLinkList.append(link)
            elif button_text == "Connect":
                connectCount += 1
                page.keyboard.press("Enter")
                page.get_by_text("Send without a note").click()
            elif button_text == "Follow":
                connectLinkList.append(link)
                followCount += 1
            elif button_text == "Pending":
                pendingCount += 1
                pass  # Nothing to do here
            sleep(0.5)
        if remainder == 0 and a == numberOfPages - 1:
            break
        page.get_by_label("Next").click()
        sleep(2)
    for a in range(remainder):
        page.keyboard.press("Tab")
        sleep(0.4)
        name = page.evaluate("document.activeElement.innerText")
        if name == "LinkedIn Member":
            linkedInMemberCount += 1
            continue
        link = page.evaluate("document.activeElement.href")
        page.keyboard.press("Tab")
        sleep(0.4)
        button_text = page.evaluate("document.activeElement.innerText")
        if button_text not in ["Message", "Connect", "Follow", "Pending"]:
            page.keyboard.press("Tab")
            sleep(0.4)
            button_text = page.evaluate("document.activeElement.innerText")
        if button_text == "":
            page.keyboard.press("Tab")
            sleep(0.4)
            button_text = page.evaluate("document.activeElement.innerText")
        if button_text == "Message":
            messageCount += 1
            connectLinkList.append(link)
        elif button_text == "Connect":
            connectCount += 1
            page.keyboard.press("Enter")
            page.get_by_text("Send without a note").click()
        elif button_text == "Follow":
            connectLinkList.append(link)
            followCount += 1
        elif button_text == "Pending":
            pendingCount += 1
            pass  # Nothing to do here
        sleep(0.5)
    sleep(1)

    for a in connectLinkList:
        if validators.url(a):
            page.goto(a)
            page.get_by_role("button", name="More actions").click()
            while True:
                page.keyboard.press("Tab")
                button_text = page.evaluate("document.activeElement.innerText")
                if button_text == "Connect":
                    page.keyboard.press("Enter")
                    break
            page.get_by_text("Send without a note").click()
            print("connected")
            sleep(1)
