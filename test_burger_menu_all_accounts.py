from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

BASE_URL = "https://www.saucedemo.com/"
PASSWORD = "secret_sauce"

# Liste des comptes
ACCOUNTS = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user"
]

# Liens du menu
MENU_LINKS = {
    "All Items": "inventory_sidebar_link",
    "About": "about_sidebar_link",
    "Logout": "logout_sidebar_link",
    "Reset App State": "reset_sidebar_link"
}

def js_click(driver, element):
    driver.execute_script("arguments[0].click();", element)

def login(driver, username):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "user-name").clear()
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "login-button").click()

def test_menu_for_account(username):

    print("\n====================================================")
    print(f"🚀 TEST DU COMPTE : {username}")
    print("====================================================")

    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        login(driver, username)

        # Compte locked → arrêt du test
        if username == "locked_out_user":
            error_msg = driver.find_element(By.CSS_SELECTOR, ".error-message-container").text
            print(f"❌ Compte bloqué : {error_msg}")
            driver.quit()
            return

        # Attendre l’apparition des produits
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
        )
        print("✅ Connexion réussie")

        # Ouvrir le menu
        driver.find_element(By.ID, "react-burger-menu-btn").click()
        print("📂 Menu ouvert")
        time.sleep(1)

        # Tester tous les liens
        for link_name, link_id in MENU_LINKS.items():

            print(f"\n➡ Test du lien : {link_name}")

            # Réouvrir le menu si fermé
            try:
                menu_panel = driver.find_element(By.CLASS_NAME, "bm-menu")
                if not menu_panel.is_displayed():
                    driver.find_element(By.ID, "react-burger-menu-btn").click()
            except:
                driver.find_element(By.ID, "react-burger-menu-btn").click()

            link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, link_id))
            )
            js_click(driver, link)
            print(f"   👉 Clic sur '{link_name}'")
            time.sleep(1)

            # COMPORTEMENTS SPÉCIAUX
            if link_name == "About":
                WebDriverWait(driver, 10).until(EC.url_contains("saucelabs.com"))
                print("   ✔ Redirection SauceLabs OK")
                driver.back()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
                )

            elif link_name == "Logout":
                time.sleep(1)
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "login-button"))
                )
                print("   ✔ Déconnexion OK")
                return  # on arrête ce compte ici

            elif link_name == "Reset App State":
                print("   ✔ Reset App State OK")

            elif link_name == "All Items":
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
                )
                print("   ✔ Retour All Items OK")

        print("\n🎉 Fin des tests pour :", username)

    except Exception as e:
        print("❌ ERREUR durant le test :", e)

    finally:
        driver.quit()


# LANCEMENT DU TEST POUR TOUS LES COMPTES
for account in ACCOUNTS:
    test_menu_for_account(account)