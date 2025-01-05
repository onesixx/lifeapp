from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def open_url_and_perform_actions(url, button_selector, input_selector, text_to_input, click_time):
    # Initialize the Chrome driver
    driver = webdriver.Chrome()

    # Open the URL
    driver.get(url)

    # Wait until the specified time to click the button
    while True:
        current_time = time.strftime("%H:%M:%S")
        if current_time >= click_time:
            break
        time.sleep(1)

    # Find the button and click it
    button = driver.find_element(By.CSS_SELECTOR, button_selector)
    button.click()

    # Find the input field and enter the text
    input_field = driver.find_element(By.CSS_SELECTOR, input_selector)
    input_field.send_keys(text_to_input)

    # Optionally, submit the form if needed
    input_field.send_keys(Keys.RETURN)

    # Keep the browser open for a while to see the result
    time.sleep(10)

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    url = "https://example.com"
    button_selector = "#button-id"  # Replace with the actual CSS selector of the button
    input_selector = "#input-id"    # Replace with the actual CSS selector of the input field
    text_to_input = "Hello, World!"
    click_time = "15:30:00"         # Replace with the desired time in HH:MM:SS format

    open_url_and_perform_actions(url, button_selector, input_selector, text_to_input, click_time)