from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()

def press_escape_key():
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def handle_popups():
    while True:
        try:
            # Check for and handle the sign-up pop-up
            sign_up_popup_close = WebDriverWait(driver, 0.5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'largeBannerCloser'))
            )
            press_escape_key()
            print("Pressed escape for sign-up pop-up.")
        except Exception as e:
            print("No sign-up pop-up found or failed to close it.")

        try:
            close_button = WebDriverWait(driver, 0.5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'button2'))
            )
            press_escape_key()
            print("Pressed escape for general pop-up.")
            driver.switch_to.default_content()
        except Exception as e:
            print("No general pop-up found or failed to close it.")

        try:
            # Check for and handle the sidebar overlay lightbox
            sidebar_overlay_lightbox = WebDriverWait(driver, 0.5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[id^='sidebar-overlay-lightbox']"))
            )
            driver.execute_script("arguments[0].style.display = 'none';", sidebar_overlay_lightbox)
            print("Removed sidebar overlay lightbox.")
        except Exception as e:
            print("No sidebar overlay lightbox found or failed to remove it.")
        
        # Break if no pop-ups are found
        break

def click_next_page():
    try:
        next_arrow = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'blueRightSideArrowPaginationIcon'))
        )
        next_arrow.click()
        print("Clicked next page arrow.")
        return True
    except Exception as e:
        print(f"Failed to click next page arrow: {e}")
        return False

# Function to extract company links from the current page
def extract_company_links():
    company_data = []

    print("Extracting company links from current page")
    handle_popups()
    
    # Extract company name, industry, and URL
    rows = driver.find_elements(By.CSS_SELECTOR, 'tr')
    testcount = 0
    for row in rows:
        testcount += 1
        try:
            company_name = row.find_element(By.CSS_SELECTOR, 'td[data-column-name="name_trans"] a').text
            base_url = row.find_element(By.CSS_SELECTOR, 'td[data-column-name="name_trans"] a').get_attribute('href')
            industry_element = row.find_element(By.CSS_SELECTOR, 'td[data-column-name="industry_trans"]')

            # Split the URL to insert '-ratios' before the query parameters
            if '?' in base_url:
                url_parts = base_url.split('?')
                company_url = f"{url_parts[0]}-ratios?{url_parts[1]}"
            else:
                company_url = f"{base_url}-ratios"

            # Use JavaScript to get the text from the hidden element
            industry = driver.execute_script("return arguments[0].innerText;", industry_element).strip()

            company_data.append({"Company Name": company_name, "URL": company_url, "Industry": industry})
        except:
            continue

    return company_data

# Function to extract ratios data 
def extract_ratios_data(url):
    print(url)
    driver.get(url)
    try:
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.genTbl.reportTbl'))
        )
    except Exception as e:
        print(f"Element not found for {url}: {e}")
        return {}
    
    ratios = {}
    
    try:
        table = driver.find_element(By.CSS_SELECTOR, 'table.genTbl.reportTbl')
        rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')
        
        for row in rows:
            columns = row.find_elements(By.CSS_SELECTOR, 'td')
            if len(columns) == 3:
                ratio_name = columns[0].text.strip()
                company_value = columns[1].text.strip()
                industry_value = columns[2].text.strip()
                
                ratios[ratio_name] = {
                    'Company': company_value,
                    'Industry': industry_value
                }
    except Exception as e:
        print(f"Failed to extract ratios from {url}: {e}")
    
    return ratios



def scraping():
    page_counter = 1
    all_data = []

    while True:
        print(f"Scraping page {page_counter}")
        handle_popups()

        try:
            pagination_selected = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.pagination.selected"))
            ).text
            if pagination_selected == '1' and page_counter != 1:
                print("Pagination reset detected, stopping scraping.")
                break
        except Exception as e:
            print(f"Failed to find pagination selected element: {e}")
            # If we can't find the pagination element, we might be on the last page
            if page_counter != 1:
                print("Assuming end of pagination, stopping scraping.")
                break
            
        data = extract_company_links()
        all_data.extend(data)

        if not click_next_page():
            handle_popups()
        else:
            page_counter += 1
        time.sleep(1)  # Small delay to prevent overwhelming the server
    return all_data

if __name__ == "__main__":
    driver.get("https://www.investing.com/stock-screener/?sp=country::5|sector::a|industry::a|equityType::a|exchange::a%3Ceq_market_cap;1")
    final_data = []
    all_data = scraping()
    print(all_data)

    df = pd.DataFrame(all_data)
    df.to_csv('company_links.csv', index=False)
    print("Company data saved to company_data.csv")
