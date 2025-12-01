from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# -----------------------------
# CONFIGURATION CHROME
# -----------------------------
def get_chrome_options():
    options = Options()
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
        "profile.default_content_setting_values.notifications": 2
    })
    return options


# -----------------------------
# FERMER POPUP DU SITE
# -----------------------------
def close_password_alert_if_present(driver):
    try:
        alert_btn = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='OK']"))
        )
        alert_btn.click()
        print("🔕 Popup mot de passe fermé automatiquement.")
    except:
        pass


# -----------------------------
# LOGIN
# -----------------------------
def login(driver, username):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()


# -----------------------------
# FONCTIONS PRIX
# -----------------------------
def get_catalog_price(driver, product):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//div[text()='{product}']"))
    )
    price_text = driver.find_element(
        By.XPATH,
        f"//div[text()='{product}']/ancestor::div[@class='inventory_item']//div[@class='inventory_item_price']"
    ).text
    return float(price_text.replace("$", ""))


def get_cart_price(driver):
    return float(driver.find_element(By.CLASS_NAME, "inventory_item_price").text.replace("$", ""))


def get_checkout_price(driver):
    prices = driver.find_elements(By.CSS_SELECTOR, ".inventory_item_price")
    return float(prices[-1].text.replace("$", ""))


# -----------------------------
# AJOUTER PRODUIT
# -----------------------------
def add_product_to_cart(driver, product):
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//div[text()='{product}']/ancestor::div[@class='inventory_item']//button"))
    )
    btn.click()


# -----------------------------
# TEST PRINCIPAL PAR COMPTE
# -----------------------------
def test_price_consistency_for_account(username):
    print(f"➡️ Démarrage du test pour : {username}")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=get_chrome_options()
    )
    driver.maximize_window()

    product = "Sauce Labs Backpack"

    # LOGIN
    login(driver, username)
    close_password_alert_if_present(driver)

    # Vérifier si utilisateur bloqué
    try:
        driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
        print(f"⚠️ UTILISATEUR BLOQUÉ : {username} — Test ignoré")
        driver.quit()
        return
    except:
        pass

    # -----------------------------
    # TEST 1 : Catalogue → Panier
    # -----------------------------
    print("\n🟦 TEST 1 : Catalogue → Panier")

    price_catalog = get_catalog_price(driver, product)
    print(f"  ➡️ Prix catalogue : {price_catalog}$")

    add_product_to_cart(driver, product)

    driver.find_element(By.ID, "shopping_cart_container").click()
    price_cart = get_cart_price(driver)
    print(f"  ➡️ Prix panier    : {price_cart}$")

    if price_catalog == price_cart:
        print("  ✅ PASS — Catalogue = Panier")
    else:
        print("  ❌ FAIL — Catalogue ≠ Panier")

    # -----------------------------
    # TEST 2 : Panier → Checkout
    # -----------------------------
    print("\n🟩 TEST 2 : Panier → Checkout")

    try:
        driver.find_element(By.ID, "checkout").click()
        driver.find_element(By.ID, "first-name").send_keys("Iram")
        driver.find_element(By.ID, "last-name").send_keys("Ksila")
        driver.find_element(By.ID, "postal-code").send_keys("2050")

        driver.find_element(By.ID, "continue").click()

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".inventory_item_price"))
        )

        price_checkout = get_checkout_price(driver)
        print(f"  ➡️ Prix checkout  : {price_checkout}$")

        if price_checkout == price_cart:
            print("  ✅ PASS — Panier = Checkout")
        else:
            print("  ❌ FAIL — Panier ≠ Checkout")

    except:
        print("  ❌ Continue ne fonctionne pas — impossible d’atteindre le résumé du checkout")
        driver.quit()
        return

    # -----------------------------
    # COMPARAISON FINALE
    # -----------------------------
    print("\n📊 COMPARAISON FINALE DES 3 PRIX :")
    print(f"  Catalogue : {price_catalog}$")
    print(f"  Panier    : {price_cart}$")
    print(f"  Checkout  : {price_checkout}$")

    print("\n--------------------------------------------")
    if price_catalog == price_cart == price_checkout:
        print("🎉 Tous les prix sont identiques !")
    else:
        if price_catalog != price_cart:
            print("❗ Catalogue ≠ Panier")
        if price_cart != price_checkout:
            print("❗ Panier ≠ Checkout")
        if price_catalog != price_checkout:
            print("❗ Catalogue ≠ Checkout")
    print("--------------------------------------------")

    driver.quit()


# -----------------------------
# TEST POUR TOUS LES COMPTES
# -----------------------------
def run_test_for_all_accounts():
    accounts = [
        "standard_user",
        "locked_out_user",
        "problem_user",
        "performance_glitch_user",
        "error_user",
        "visual_user"
    ]

    for account in accounts:
        print("\n" + "=" * 60)
        print(f"🔵 TEST AVEC LE COMPTE : {account}")
        print("=" * 60)
        test_price_consistency_for_account(account)


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    run_test_for_all_accounts()









