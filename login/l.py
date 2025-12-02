import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --------------------------------------------------
# Configuration + dossier screenshots
# --------------------------------------------------
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 20)

if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

def slow_print(text):
    print(text)
    time.sleep(1.5)

def take_screenshot(name):
    driver.save_screenshot(f"screenshots/{name}.png")
    slow_print(f"📸 Screenshot enregistré : {name}.png")

def open_login_page():
    driver.get("https://www.saucedemo.com/")
    wait.until(EC.presence_of_element_located((By.ID, "user-name")))
    slow_print("➡️ Page Login ouverte")

# --------------------------------------------------
# Fonction générique pour tester un login
# --------------------------------------------------
def test_login(username, password, scenario_name):
    try:
        slow_print(f"\n===== {scenario_name} =====")
        open_login_page()

        if username:
            driver.find_element(By.ID, "user-name").send_keys(username)
            slow_print(f"🟦 Username saisi : {username}")

        if password:
            driver.find_element(By.ID, "password").send_keys(password)
            slow_print("🟦 Password saisi")

        driver.find_element(By.ID, "login-button").click()
        slow_print("🟦 Bouton Login cliqué")

        # Cas spéciaux des utilisateurs
        if username == "locked_out_user":
            error = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@data-test='error']")))
            assert "locked out" in error.text.lower()
            slow_print(f"✔️ Utilisateur verrouillé détecté : {error.text}")

        elif username == "problem_user":
            wait.until(EC.url_contains("inventory"))
            slow_print("✔️ Login réussi pour problem_user (UI peut avoir des bugs)")

        elif username == "performance_glitch_user":
            wait.until(EC.url_contains("inventory"))
            slow_print("✔️ Login réussi pour performance_glitch_user (très lent)")

        elif username == "error_user":
            wait.until(EC.url_contains("inventory"))
            slow_print("✔️ Login réussi pour error_user (des erreurs peuvent apparaître)")

        elif username == "visual_user":
            wait.until(EC.url_contains("inventory"))
            slow_print("✔️ Login réussi pour visual_user (problèmes visuels)")

        # Login standard
        elif username == "standard_user" and password == "secret_sauce":
            wait.until(EC.url_contains("inventory"))
            slow_print("✔️ Login réussi pour standard_user")

        # Cas d'erreur général (mot de passe incorrect ou username inexistant)
        else:
            error = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@data-test='error']")))
            slow_print(f"✔️ Message d’erreur affiché : {error.text}")

        # Screenshot à la fin du test
        take_screenshot(scenario_name)

    except Exception as e:
        slow_print(f"❌ Échec {scenario_name} : {e}")
        take_screenshot(f"{scenario_name}_error")

# --------------------------------------------------
# EXÉCUTION DES SCÉNARIOS
# --------------------------------------------------
# Tous les utilisateurs officiels
users = [
    ("standard_user", "secret_sauce", "TC01_StandardUser"),
    ("locked_out_user", "secret_sauce", "TC02_LockedOutUser"),
    ("problem_user", "secret_sauce", "TC03_ProblemUser"),
    ("performance_glitch_user", "secret_sauce", "TC04_PerformanceGlitchUser"),
    ("error_user", "secret_sauce", "TC05_ErrorUser"),
    ("visual_user", "secret_sauce", "TC06_VisualUser"),
]

# Scénarios supplémentaires d'erreurs
additional_tests = [
    ("standard_user", "wrong_pass", "TC07_PasswordIncorrect"),
    ("abc123", "secret_sauce", "TC08_UsernameInexistant"),
    ("", "", "TC09_ChampsVides"),
    ("", "secret_sauce", "TC10_UsernameVide"),
    ("standard_user", "", "TC11_PasswordVide"),
]

# Exécution des tests utilisateurs officiels
for u in users:
    test_login(u[0], u[1], u[2])

# Exécution des tests supplémentaires
for t in additional_tests:
    test_login(t[0], t[1], t[2])

slow_print("\n🎉 Tous les tests login sont terminés !")

driver.quit()
