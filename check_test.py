from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Liste des comptes à tester
accounts = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user"
]

password = "secret_sauce"

for user in accounts:
    print(f"===== TEST COMPTE : {user} =====")

    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")

    # Login
    driver.find_element(By.ID, "user-name").send_keys(user)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

    # Vérifier si compte bloqué
    try:
        error_msg = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text
        print(f"❌ ECHEC LOGIN : {error_msg}")
        driver.quit()
        print()
        continue
    except NoSuchElementException:
        print("✔ Login réussi")

    # Essayer d’ajouter au panier
    try:
        add_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
        )
        add_button.click()
        print("✔ Article ajouté")
    except TimeoutException:
        print("❌ Impossible d'ajouter l'article")
        driver.quit()
        print()
        continue

    # Aller au panier
    driver.find_element(By.ID, "shopping_cart_container").click()

    # Vérifier le bouton Checkout
    try:
        checkout_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        print("✔ Checkout disponible")
        checkout_btn.click()
        print("✔ Test Checkout PASS")
    except TimeoutException:
        print("❌ Checkout non disponible")

    driver.quit()
    print()

