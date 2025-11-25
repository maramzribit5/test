from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def test_add_to_cart_design():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.saucedemo.com/")

    # LOGIN visual_user
    driver.find_element(By.ID, "user-name").send_keys("visual_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Tous les boutons Add to cart
    buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn_inventory")

    # ---- TC-ADD-01 : Alignement ----
    x_positions = [btn.location['x'] for btn in buttons]
    assert len(set(x_positions)) == 1, "❌ FAIL - Alignement incorrect"

    # ---- TC-ADD-02 : Couleur ----
    colors = [btn.value_of_css_property("background-color") for btn in buttons]
    assert len(set(colors)) == 1, "❌ FAIL - Couleurs différentes"

    # ---- TC-ADD-03 : Taille ----
    sizes = [(btn.size['width'], btn.size['height']) for btn in buttons]
    assert len(set(sizes)) == 1, "❌ FAIL - Taille incohérente"

    # ---- TC-ADD-04 : Lisibilité ----
    font_sizes = [btn.value_of_css_property("font-size") for btn in buttons]
    assert len(set(font_sizes)) == 1, "❌ FAIL - Police non uniforme"

    # ---- TC-ADD-05 : Hover ----
    first_btn = buttons[0]
    original_color = first_btn.value_of_css_property("background-color")

    ActionChains(driver).move_to_element(first_btn).perform()
    hover_color = first_btn.value_of_css_property("background-color")

    assert original_color != hover_color, "❌ FAIL - Hover non fonctionnel"

    driver.quit()
