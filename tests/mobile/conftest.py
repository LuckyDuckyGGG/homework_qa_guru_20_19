import allure
import pytest
import allure_commons
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from dotenv import load_dotenv
from selene import browser, support
import os
import requests



@pytest.fixture(autouse=True)
def load_env():
    load_dotenv()


def attach_bstack_video(session_id):
    bstack_session = requests.get(
    f'https://api.browserstack.com/app-automate/sessions/{session_id}.json',
    auth=(os.getenv('USER_NAME'), os.getenv('ACCESS_KEY')),
    ).json()
    print(bstack_session)
    video_url = bstack_session['automation_session']['video_url']

    allure.attach(
            '<html><body>'
            '<video width="100%" height="100%" controls autoplay>'
            f'<source src="{video_url}" type="video/mp4">'
            '</video>'
            '</body></html>',
            name='video recording',
            attachment_type=allure.attachment_type.HTML,
        )


@pytest.fixture(scope='function', autouse=True)
def mobile_management(request):
    if hasattr(browser, 'driver') and browser.driver:
        try:
            browser.driver.quit()
        except:
            pass
        browser.config.driver = None

    options = UiAutomator2Options().load_capabilities({
            'platformName': 'Android',
            'platformVersion': '12.0',
            'deviceName': 'Samsung Galaxy S22 Ultra',
            'app': 'bs://c4135d768e0c45d3cd9368d1f1cf1c0c5545caa5',
            'appium:fullReset': True,
            'bstack:options': {
                'projectName': 'Android Project',
                'buildName': 'android-build-1',
                'sessionName': 'Android Test',
                'userName': os.getenv("USER_NAME"),
                'accessKey': os.getenv("ACCESS_KEY")
            }
        })

    browser.config.driver_remote_url = os.getenv("BASE_URL")
    browser.config.driver_options = options
    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG,
    )

    allure.attach(
        browser.driver.page_source,
        name='screen xml dump',
        attachment_type=allure.attachment_type.XML,
    )

    session_id = browser.driver.session_id

    browser.driver.quit()
    browser.config.driver = None

    attach_bstack_video(session_id)