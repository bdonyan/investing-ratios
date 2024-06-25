import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import logging
from datetime import datetime

# Setup Chrome options to ignore SSL certificate errors
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

# Setup the Chrome driver with the options
service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

# Function to extract ratios data 
def extract_ratios_data(url, count):
    print(f"{count}. {url} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    driver.get(url)
    try:
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.genTbl.reportTbl'))
        )
    except Exception as e:
        logging.error(f"Element not found for {url}: {e}")
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

if __name__ == "__main__":
    df = pd.read_csv('company_links.csv')
    all_data = df.to_dict('records')
    final_data = []

    for count, data in enumerate(all_data, start=1):
        url = data["URL"]
        ratios = extract_ratios_data(url, count)
        row = {"Company Name": data["Company Name"], "Industry": data["Industry"]}
        for ratio_name, values in ratios.items():
            row[f"{ratio_name} (Company)"] = values['Company']
            row[f"{ratio_name} (Industry)"] = values['Industry']
        final_data.append(row)
    
    df_final = pd.DataFrame(final_data)

    # Remove the 3rd and 4th columns from the output DataFrame if they exist
    if len(df_final.columns) > 4:
        df_final.drop(columns=[df_final.columns[2], df_final.columns[3]], inplace=True)
    
    df_final.to_csv('company_ratios.csv', index=False)
    print("Data saved to company_ratios.csv")

# Close the driver
driver.quit()
