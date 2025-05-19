import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# def get_token_and_company_id(username, password):
#     driver = webdriver.Chrome()
#     driver.get("https://tankhwapatra.co.in/#/user/login")
#     time.sleep(2)

#     driver.find_element(By.NAME, "phone").send_keys(username)
#     driver.find_element(By.NAME, "password").send_keys(password)
#     driver.find_element(By.CSS_SELECTOR, ".button.btn-primary.fs16").click()
#     time.sleep(5)

#     token, company_id = None, None
#     keys = driver.execute_script("return Object.keys(localStorage);")
#     for key in keys:
#         if key in ['token', 'company_id']:
#             value = driver.execute_script(f"return localStorage.getItem('{key}');")
#             if key == 'token':
#                 token = value
#             elif key == 'company_id':
#                 company_id = int(value)  # Make sure it's an integer

#     driver.quit()
#     return token, company_id

def get_users_by_search_query(token, company_id,intent, search_query):
    if not token or not company_id:
        raise Exception("Failed to retrieve token or company ID.")

    data = {
        "companyMasterID": company_id,
        "status": 1,
        "searchQuery": search_query
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    if intent == "get_personal_info":
        url = "https://apitankhwapatra.tankhwapatra.co.in/companycontact/v1/getAllUsers"

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed: {response.status_code} {response.text}")


