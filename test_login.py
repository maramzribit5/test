from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Crée le navigateur Chrome
driver = webdriver.Chrome()
driver.maximize_window()


# Compteurs
tests_passed = 0
tests_failed = 0

print("=" * 50)
print("DÉBUT DES TESTS - FONCTIONNALITÉ LOGIN")
print("=" * 50)

# ----------------------------
# TC01 : LOGIN VALIDE
# ----------------------------
print("\n[TC01] Test de login valide...")
try:
    driver.get("https://www.saucedemo.com/")

    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("/inventory.html")
    )
    print("✔ TC01 PASS - Redirection vers inventaire réussie")
    tests_passed += 1
    
    # Déconnexion
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    time.sleep(1)
    driver.find_element(By.ID, "logout_sidebar_link").click()
    time.sleep(1)
    
except Exception as e:
    print("✘ TC01 FAIL")
    driver.save_screenshot("TC01_fail.png")
    tests_failed += 1


# ----------------------------
# TC02 : MAUVAIS PASSWORD
# ----------------------------
print("\n[TC02] Test avec mot de passe incorrect...")

try:
    driver.get("https://www.saucedemo.com/")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )

    username = driver.find_element(By.ID, "user-name")
    password = driver.find_element(By.ID, "password")

    username.clear()
    password.clear()

    username.send_keys("standard_user")
    password.send_keys("wrongpassword")

    driver.find_element(By.ID, "login-button").click()

    error_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    )
    errorMsg = error_element.text

    print(" Message reçu :", errorMsg)

    if "do not match" in errorMsg:
        print("✔ TC02 PASS - Message correct")
        tests_passed += 1
    else:
        print("✘ TC02 FAIL - Mauvais message affiché")
        tests_failed += 1

except Exception as e:
    print("✘ TC02 FAIL - Erreur détectée :", e)
    driver.save_screenshot("TC02_fail.png")
    tests_failed += 1


# ----------------------------
# TC03 : USERNAME VIDE
# ----------------------------
print("\n[TC03] Test avec username vide...")

try:
    driver.get("https://www.saucedemo.com/")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )

    username = driver.find_element(By.ID, "user-name")
    password = driver.find_element(By.ID, "password")

    username.clear()
    password.clear()

    password.send_keys("secret_sauce")  # username vide
    driver.find_element(By.ID, "login-button").click()

    error_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    )
    errorMsg = error_element.text

    print(" Message reçu :", errorMsg)

    if "Username is required" in errorMsg:
        print("✔ TC03 PASS - Message correct")
        tests_passed += 1
    else:
        print("✘ TC03 FAIL - Mauvais message affiché")
        tests_failed += 1

except Exception as e:
    print("✘ TC03 FAIL - Erreur détectée :",e)
    driver.save_screenshot("TC03_fail.png")
    tests_failed += 1


# ----------------------------
# TC04 : PASSWORD VIDE
# ----------------------------
print("\n[TC04] Test avec password vide...")

try:
    driver.get("https://www.saucedemo.com/")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )

    username = driver.find_element(By.ID, "user-name")
    password = driver.find_element(By.ID, "password")

    username.clear()
    password.clear()

    username.send_keys("standard_user")  # password vide
    driver.find_element(By.ID, "login-button").click()

    error_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    )
    errorMsg = error_element.text

    print(" Message reçu :", errorMsg)

    if "Password is required" in errorMsg:
        print("✔ TC04 PASS - Message correct")
        tests_passed += 1
    else:
        print("✘ TC04 FAIL - Mauvais message affiché")
        tests_failed += 1

except Exception as e:
    print("✘ TC04 FAIL - Erreur détectée :", e)
    driver.save_screenshot("TC04_fail.png")
    tests_failed += 1




# ----------------------------
# TC05 : UTILISATEUR BLOQUÉ
# ----------------------------
print("\n[TC05] Test utilisateur bloqué...")
try:
    driver.get("https://www.saucedemo.com/")

    driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    errorMsg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    ).text

    print(f"   Message reçu : '{errorMsg}'")

    if "locked out" in errorMsg:
        print("✔ TC05 PASS - Utilisateur bloqué détecté")
        tests_passed += 1
    else:
        print("✘ TC05 FAIL - Message incorrect")
        tests_failed += 1

except Exception:
    print("✘ TC05 FAIL - Erreur détectée")
    driver.save_screenshot("TC05_fail.png")
    tests_failed += 1


# ----------------------------
# RAPPORT FINAL
# ----------------------------
print("\n" + "=" * 50)
print("RAPPORT D'EXÉCUTION")
print("=" * 50)
print(f" Tests réussis : {tests_passed}/5")
print(f" Tests échoués : {tests_failed}/5")
print(f" Taux de réussite : {(tests_passed/5)*100:.0f}%")
print("=" * 50)

# Fermeture
time.sleep(8)
driver.quit()
print("\n✔ Navigateur fermé - Tests terminés")
