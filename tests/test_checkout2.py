from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ------------------------------
# LOGIN
# ------------------------------
def login(driver, username):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()


# ------------------------------
# AJOUTER PREMIER PRODUIT
# ------------------------------
def add_first_item(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
    )
    first_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_inventory"))
    )
    first_btn.click()


# ------------------------------
# RÉCUPERER POSITION Y DU CHECKOUT
# ------------------------------
def get_checkout_position(username):
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.maximize_window()

    try:
        # LOGIN
        login(driver, username)

        # Vérifier compte bloqué
        try:
            driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
            print(f"⚠️ Compte bloqué : {username} — Test ignoré")
            driver.quit()
            return None
        except:
            pass

        # Ajouter produit
        add_first_item(driver)

        # Ouvrir panier
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "shopping_cart_container"))
        ).click()

        # Trouver Checkout
        checkout_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "checkout"))
        )

        y_position = checkout_button.location["y"]
        driver.quit()
        return y_position

    except Exception as e:
        print(f"❌ ERREUR pour {username} : {e}")
        driver.quit()
        return None


# ------------------------------
# TEST POUR LES 6 COMPTES
# ------------------------------
def test_checkout_button_all_accounts():

    print("\n🔵 Test de la position du bouton Checkout pour les 6 comptes...\n")

    # ----- LES 6 COMPTES -----
    accounts = [
        "standard_user",
        "locked_out_user",
        "problem_user",
        "performance_glitch_user",
        "error_user",
        "visual_user"
    ]

    positions = {}

    # 1) Récupération des positions
    for acc in accounts:
        print(f"➡️ Récupération position pour : {acc}")
        pos = get_checkout_position(acc)
        positions[acc] = pos
        print(f"   ➜ Position : {pos}\n")

    # Position de référence = standard_user
    ref = positions["standard_user"]

    print("\n====================================================")
    print("📊 RÉSULTATS COMPARATIFS DES 6 COMPTES")
    print("====================================================")

    for acc, pos in positions.items():

        if pos is None:
            print(f"⚠️ {acc} : Test non applicable (bloqué ou erreur)")
            continue

        diff = abs(pos - ref)
        if diff <= 5:
            print(f"✅ {acc} : Position correcte (Y = {pos}) — Diff = {diff}px")
        else:
            print(f"❌ {acc} : Position INCORRECTE (Y = {pos}) — Diff = {diff}px")

    print("====================================================")


# ------------------------------
# MAIN
# ------------------------------
if __name__ == "__main__":
    test_checkout_button_all_accounts()
