from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
option = Options()
option.add_argument("--window-size=1400,960")

import pandas as pd
import time

def google_search_with_selenium(query, driver):
    

    # 開啟Google
    driver.get("https://cse.google.com/cse?cx=117856f7b40b74cf8")

    # 找到搜尋框並輸入查詢詞
    search_box = driver.find_element(By.ID, "gsc-i-id1") # gsc-i-id1
    search_box.send_keys(query)

    # 找到搜尋按鈕並點擊
    search_button = driver.find_element(By.CLASS_NAME, "gsc-search-button-v2")
    
    time.sleep(1)
    # search_box.submit()
    search_button.click()
    time.sleep(1)

    # get first result
    link = "-"
    try:
        first_result = driver.find_element(By.CSS_SELECTOR, "#___gcse_0 > div > div > div > div.gsc-wrapper > div.gsc-resultsbox-visible > div.gsc-resultsRoot.gsc-tabData.gsc-tabdActive > div > div.gsc-expansionArea > div:nth-child(1) > div > div.gsc-thumbnail-inside > div > a")
        if first_result:
            link = first_result.get_attribute("href")
            print(f"[INFO] {link}")
    except Exception as e:
        print(f"[ERROR] {e}")

    return link

if __name__ == '__main__':
    try:
        print(f"[INFO] START {'*'*20}")

        driver = webdriver.Chrome(options=option)

        # load csv
        df_organizations = pd.read_csv('support_organizations.csv', encoding='shift_jis')
        df_list = pd.read_csv('list.csv', encoding='shift_jis')
        support_organizations = df_organizations['name'].tolist()

        df_results = pd.DataFrame(columns=["city", "town"] + support_organizations)

        for index, row in df_list.iterrows():
            results_row = [row['city'], row['town']]
            print(f"[INFO][{index}] CHECK:{row['city']} {row['town']}")

            for organization in support_organizations:
                query = f"{row['city']} {row['town']} {organization}"
                link = google_search_with_selenium(query, driver)
                results_row.append(link)

            df_results.loc[len(df_results)] = results_row

        df_results.to_csv("google_search_results.csv", index=False)

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        print(f"[INFO] END {'*'*20}")
        
        # close browser
        driver.quit()
