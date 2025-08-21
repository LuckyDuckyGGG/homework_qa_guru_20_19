import allure
import pytest
from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have, be


def test_search_android():

    with step('Пропускаем туториал'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/fragment_onboarding_skip_button')).click()

    with step('Ищем значение browserstack в поиске'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/search_src_text')).type('BrowserStack')

    with step('Проверяем результат поиска'):
        search_results = browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title'))
        search_results.should(have.size_greater_than(0))
        search_results.first.should(have.text('BrowserStack'))

def test_open_article_android():

    with step('Пропускаем туториал'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/fragment_onboarding_skip_button')).click()

    with step('Ищем значение browserstack в поиске'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/search_src_text')).type('BrowserStack')

    with step('Открываем найденную статью'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title')).click()

    with step('Закрываем всплывающие модалки'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/closeButton')).click()
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/page_contents_container')).click()

    with step('Проверяем заголовок открытой статьи'):
        browser.element('//android.widget.TextView[@text="BrowserStack"]').should(have.text("BrowserStack"))
