from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


# ------------------------------------------------------
# CONFIG CHROME (100% anti popups Google)
# ------------------------------------------------------
def get_chrome_options():
    options = Options()
    options.add_argument("--start-maximized")

    # 🔒 Désactiver toutes les alertes mot de passe
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
    })

    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-features=PasswordLeakDetection")
    return options


# ------------------------------------------------------
# FERMER POPUP GOOGLE SI PRÉSENT
# ------------------------------------------------------
def close_password_popup(driver):
    try:
        alert_btn = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='OK']"))
        )
        alert_btn.click()
        print("🔕 Popup Google fermé automatiquement.")
    except:
        pass


# ------------------------------------------------------
# LOGIN
# ------------------------------------------------------
def login(driver, username):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # fermer popup immédiatement si affiché
    close_password_popup(driver)


# ------------------------------------------------------
# TEST POUR 6 BOUTONS
# ------------------------------------------------------
def test_add_remove_buttons_for_account(username):

    print(f"\n===================================================")
    print(f"🧪 TEST POUR LE COMPTE : {username}")
    print("===================================================\n")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=get_chrome_options()
    )

    # LOGIN
    login(driver, username)

    # utilisateur bloqué
    try:
        driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
        print(f"⚠️ {username} est BLOQUÉ — aucun test possible")
        driver.quit()
        return
    except:
        pass

    # attendre produits
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
    )

    results = []

    buttons = driver.find_elements(By.XPATH, "//button[contains(@class,'btn_inventory')]")

    for i, btn in enumerate(buttons[:6], start=1):
        print(f"\n🔹 TEST DU BOUTON n°{i}")

        try:
            # état initial = Add to cart ?
            if "Add to cart" not in btn.text:
                print(f"  ⚠️ Bouton {i} non initialisé en 'Add to cart'")
                results.append((i, "FAIL", "Bouton non initialisé"))
                continue

            # ------ CLIQUER Add ------
            btn.click()
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, f"(//button[contains(@class,'btn_inventory')])[{i}]"))
            )
            new_btn = driver.find_element(
                By.XPATH, f"(//button[contains(@class,'btn_inventory')])[{i}]"
            )

            # Vérifier changement → Remove
            if "Remove" not in new_btn.text:
                print("  ❌ FAIL : Ajout non réussi (Add → Remove ne fonctionne pas)")
                results.append((i, "FAIL", "Ajout non réussi"))
                continue
            else:
                print("  ✅ PASS : Ajout réussi (Add → Remove OK)")

            # ------ CLIQUER Remove ------
            try:
                new_btn.click()
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, f"(//button[contains(@class,'btn_inventory')])[{i}]"))
                )
                after = driver.find_element(
                    By.XPATH, f"(//button[contains(@class,'btn_inventory')])[{i}]"
                )

                # Vérifier retour → Add to cart
                if "Add to cart" in after.text:
                    print("  ✅ PASS : Suppression réussie (Remove → Add OK)")
                    results.append((i, "PASS", "OK"))
                else:
                    print("  ❌ FAIL : Suppression non réussie (Remove → Add ne fonctionne pas)")
                    results.append((i, "FAIL", "Suppression non réussie"))

            except:
                print("  ❌ FAIL : Impossible de supprimer l’article (Remove non cliquable)")
                results.append((i, "FAIL", "Remove non cliquable"))

        except:
            print("  ❌ FAIL : Bouton incliquable — impossible d’ajouter l’article")
            results.append((i, "FAIL", "Bouton incliquable"))

    driver.quit()

    # Résultat final
    print("\n📊 RÉSULTAT FINAL POUR", username)
    for num, status, msg in results:
        print(f"  → Bouton {num} : {status} ({msg})")


# ------------------------------------------------------
# TEST GLOBAL POUR LES 6 COMPTES
# ------------------------------------------------------
def test_all_accounts():
    accounts = [
        "standard_user",
        "locked_out_user",
        "problem_user",
        "performance_glitch_user",
        "error_user",
        "visual_user"
    ]

    for acc in accounts:
        test_add_remove_buttons_for_account(acc)


# MAIN
if __name__ == "__main__":
    test_all_accounts()



