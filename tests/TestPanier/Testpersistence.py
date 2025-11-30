from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def get_options():
    options = Options()
    options.add_argument("--start-maximized")
    return options


def login(driver, username):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()


def get_cart_badge(driver):
    try:
        return driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    except:
        return None


def test_cart_badge_for_account(username):

    print(f"\n======================================")
    print(f"🛒 TEST BADGE PANIER — COMPTE : {username}")
    print(f"======================================\n")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=get_options()
    )
    wait = WebDriverWait(driver, 10)

    login(driver, username)

    # Vérifier si compte bloqué
    try:
        driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
        print(f"⚠️ Compte {username} bloqué — test ignoré")
        driver.quit()
        return
    except:
        pass

    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item")))
    buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")

    # 1️⃣ — Ajout produit 1
    print("🟦 Ajout du 1er produit…")
    buttons[0].click()
    badge = get_cart_badge(driver)
    print(f"   → Badge : {badge}")
    print("   " + ("✅ PASS — Badge = 1" if badge == "1" else "❌ FAIL — Badge attendu = 1"))

    # 2️⃣ — Ajout produit 2
    print("\n🟦 Ajout du 2ème produit…")
    buttons[1].click()
    badge = get_cart_badge(driver)
    print(f"   → Badge : {badge}")
    print("   " + ("✅ PASS — Badge = 2" if badge == "2" else "❌ FAIL — Badge attendu = 2"))

    # 3️⃣ — Suppression d’un produit dans panier
    print("\n🟧 Suppression d’un produit…")
    driver.find_element(By.ID, "shopping_cart_container").click()

    try:
        remove_btn = driver.find_element(By.CLASS_NAME, "cart_button")
        remove_btn.click()
        print("   ✔ Produit supprimé du panier")
    except:
        print("   ❌ Impossible de supprimer un produit")
        driver.quit()
        return

    driver.get("https://www.saucedemo.com/inventory.html")  # retour propre

    badge = get_cart_badge(driver)
    print("   " + ("✅ PASS — Badge = 1 (mis à jour)" if badge == "1" else "❌ FAIL — Badge attendu = 1"))

    # 4️⃣ — Suppression du dernier article (CORRIGÉ)
    print("\n🟥 Suppression du dernier article…")

    try:
        driver.get("https://www.saucedemo.com/inventory.html")
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item")))

        buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")
        buttons[0].click()   # Add
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
        buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")
        buttons[0].click()   # Remove

        print("   ✔ Dernier article supprimé")

    except Exception as e:
        print("   ❌ Impossible de supprimer le dernier article :", e)
        driver.quit()
        return

    driver.get("https://www.saucedemo.com/inventory.html")
    badge = get_cart_badge(driver)

    print("   " + ("✅ PASS — Badge disparu → Panier vide"
                  if badge is None else
                  "❌ FAIL — Le badge aurait dû disparaître"))

    driver.quit()


def test_all_accounts():

    accounts = [
        "standard_user",
        "problem_user",
        "performance_glitch_user",
        "error_user",
        "visual_user",
        "locked_out_user"
    ]

    for acc in accounts:
        test_cart_badge_for_account(acc)


if __name__ == "__main__":
    test_all_accounts()


















