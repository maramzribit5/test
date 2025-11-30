from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# --- Configuration Chrome ---
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()

wait = WebDriverWait(driver, 10)

try:
    print(" Test Add to Cart - Démarrage")

    # --- 1. Login ---
    driver.get("https://www.saucedemo.com/")
    wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    wait.until(EC.url_contains("inventory"))
    print(" Login réussi")

    # --- 2. Vérifier que le panier est vide ---
    cart_badge_elements = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    if len(cart_badge_elements) == 0:
        print(" Panier vide au départ")
    else:
        print(" Panier non vide au départ")

    # --- 3. Ajouter un produit au panier ---
    product_add_btn = wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack")))
    product_add_btn.click()
    print(" Produit ajouté au panier")

    # --- 4. Vérifier que le compteur du panier a changé ---
    cart_badge = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    assert cart_badge.text == "1"
    print(" Compteur du panier correct (1)")

    # --- 5. Vérifier le contenu du panier ---
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    wait.until(EC.url_contains("cart"))

    cart_item = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_name")))
    assert "Sauce Labs Backpack" in cart_item.text
    print(" Produit présent dans le panier")

    print(" Test Add to Cart réussi !")

except Exception as e:
    print(" Le test Add to Cart a échoué :", e)
    driver.save_screenshot("add_to_cart_error.png")

finally:
    driver.quit()
