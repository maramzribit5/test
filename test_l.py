from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time

# Liste des comptes
accounts = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user"
]

PASSWORD = "secret_sauce"

# -------- FONCTIONS UTILES -------- #

def safe_send_keys(driver, wait, by, value, text):
    elem = wait.until(EC.visibility_of_element_located((by, value)))
    elem.clear()
    elem.send_keys(text)

def login(driver, wait, user):
    driver.get("https://www.saucedemo.com/")
    safe_send_keys(driver, wait, By.ID, "user-name", user)
    safe_send_keys(driver, wait, By.ID, "password", PASSWORD)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)

    # Vérifier si login échoué
    errors = driver.find_elements(By.CSS_SELECTOR, "h3[data-test='error']")
    if errors:
        return False, errors[0].text

    # Vérifier si login OK
    wait.until(EC.url_contains("inventory.html"))
    return True, ""

def select_sort(driver, wait, value):
    dropdown = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "product_sort_container"))
    )
    Select(dropdown).select_by_value(value)
    time.sleep(1)

def get_names(driver):
    return [e.text for e in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]

def get_prices(driver):
    return [float(e.text.replace("$", "")) for e in driver.find_elements(By.CLASS_NAME, "inventory_item_price")]


# -------- LOOP SUR LES COMPTES -------- #

for user in accounts:
    print("\n" + "="*60)
    print(f"===== TEST COMPTE : {user} =====")
    print("="*60)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    login_ok, msg = login(driver, wait, user)

    if not login_ok:
        print(f" Login échoué : {msg}")
        print("→ Les tests de tri ne seront pas exécutés pour ce compte.")
        driver.quit()
        continue

    print("✔ Login réussi")

    # TC01 - Tri A-Z
    try:
        select_sort(driver, wait, "az")
        names = get_names(driver)
        if names == sorted(names):
            print(" TC01 A-Z : PASS")
        else:
            print(" TC01 A-Z : FAIL")
    except:
        print(" TC01 A-Z : ERREUR")

    # TC02 - Tri Z-A
    try:
        select_sort(driver, wait, "za")
        names = get_names(driver)
        if names == sorted(names, reverse=True):
            print(" TC02 Z-A : PASS")
        else:
            print(" TC02 Z-A : FAIL")
    except:
        print(" TC02 Z-A : ERREUR")

    # TC03 - Prix bas → élevé
    try:
        select_sort(driver, wait, "lohi")
        prices = get_prices(driver)
        if prices == sorted(prices):
            print(" TC03 Prix bas-haut : PASS")
        else:
            print(" TC03 Prix bas-haut : FAIL")
    except:
        print(" TC03 Prix bas-haut : ERREUR")

    # TC04 - Prix élevé → bas
    try:
        select_sort(driver, wait, "hilo")
        prices = get_prices(driver)
        if prices == sorted(prices, reverse=True):
            print(" TC04 Prix haut-bas : PASS")
        else:
            print(" TC04 Prix haut-bas : FAIL")
    except:
        print(" TC04 Prix haut-bas : ERREUR")

    driver.quit()
www.saucedemo.com