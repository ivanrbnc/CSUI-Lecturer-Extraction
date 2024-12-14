from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

main_url = "https://cs.ui.ac.id/pengajar/"
driver.get(main_url)

professors_data = []

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.gdlr-core-personnel-list-button.gdlr-core-button"))
    )

    # Catch "More Detail" buttons
    detail_buttons = driver.find_elements(By.CSS_SELECTOR, "a.gdlr-core-personnel-list-button.gdlr-core-button")

    for i, button in enumerate(detail_buttons):
        try:
            detail_buttons = driver.find_elements(By.CSS_SELECTOR, "a.gdlr-core-personnel-list-button.gdlr-core-button")

            button = detail_buttons[i]
            ActionChains(driver).move_to_element(button).click(button).perform()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h3.gdlr-core-title-item-title.gdlr-core-skin-title"))
            )

            # Extract the professor's name
            try:
                name = driver.find_element(By.CSS_SELECTOR, "h3.gdlr-core-title-item-title.gdlr-core-skin-title").text
            except:
                name = '-'

            # Extract the professor's email
            try:
                email = driver.find_element(By.CSS_SELECTOR, "div.kingster-personnel-info-list.kingster-type-email").text
            except:
                email = '-'

            # Extract the professor's specialty
            try:
                specialty = driver.find_elements(By.CSS_SELECTOR, "div.gdlr-core-text-box-item.gdlr-core-item-pdlr.gdlr-core-item-pdb.gdlr-core-left-align div.gdlr-core-text-box-item-content p")[1].text
            except:
                specialty = "-"

            professors_data.append({
                "Name": name,
                "Email": email,
                "Specialty": specialty
            })

            print(f"Collected data for: {name}")

            driver.back()

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.gdlr-core-personnel-list-button.gdlr-core-button"))
            )

        except Exception as e:
            print(f"Error while processing professor {i + 1}: {e}")
            driver.get(main_url)

finally:
    driver.quit()

df = pd.DataFrame(professors_data)
df.to_excel("professors_data.xlsx", index=False)

print("Data exported to professors_data.xlsx")