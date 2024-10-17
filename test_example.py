import re
from playwright.sync_api import Page
from time import sleep


def test_example(page: Page) -> None: 
    company = "Deutsche Bank"
    location = "Greater Barcelona Metropolitan Area"
    jobTile = "HR"
    messageCount = 0
    connectCount = 0
    followCount = 0
    # location = input("Enter the location(exactly how on the web site): ")
    # jobTile = input("Enter the job title: ")
    # company = input("Enter the company name: ")
    page.goto("https://www.linkedin.com/")
    page.locator("[data-test-id=\"home-hero-sign-in-cta\"]").click()
    page.get_by_label("Email or phone").fill("meshareef19@gmail.com")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill(".-n76b*U8^vMRn_")
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
    results_text = page.get_by_text(re.compile(r"\d+ results")).inner_text()
    results_number = int(re.search(r"\d+", results_text).group())
    loops = 1  # Set the number of loops from the number of people
    for a in range(loops):
        page.keyboard.press("Tab")
        name = page.evaluate("document.activeElement.innerText")
        if name == "Try Premium Free For 1 Month":
            page.keyboard.press("Tab")
            name = page.evaluate("document.activeElement.innerText")
        link = page.evaluate("document.activeElement.href")
        page.keyboard.press("Tab")
        button = page.locator("document.activeElement")
        button_text = page.evaluate("document.activeElement.innerText")
        print(name, link, button_text)
        if button_text == "Message":
            messageCount += 1
            pass  # Nothing to do here
        elif button_text == "Connect":
            connectCount += 1
            # button.click()
            # page.get_by_text("Connect").click()
            # page.get_by_text("Send without a note").click()
            pass
        elif button_text == "Follow":
            followCount += 1
            pass  # Handle later