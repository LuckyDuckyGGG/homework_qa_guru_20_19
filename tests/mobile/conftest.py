import allure
import pytest
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from dotenv import load_dotenv
from selene import browser
import os


@pytest.fixture(autouse=True)
def load_env():
    load_dotenv()


def get_capabilities(platform):
    if platform == 'android':
        return {
            'platformName': 'Android',
            'platformVersion': '12.0',
            'deviceName': 'Samsung Galaxy S22 Ultra',
            'app': 'bs://c4135d768e0c45d3cd9368d1f1cf1c0c5545caa5',
            'bstack:options': {
                'projectName': 'Android Project',
                'buildName': 'android-build-1',
                'sessionName': 'Android Test',
                'userName': os.getenv("USER_NAME"),
                'accessKey': os.getenv("ACCESS_KEY")
            }
        }
    elif platform == 'ios':
        return {
            'platformName': 'iOS',
            'platformVersion': '16.4',
            'deviceName': 'iPhone 14',
            'app': 'bs://sample.app',
            'bstack:options': {
                'projectName': 'iOS Project',
                'buildName': 'ios-build-1',
                'sessionName': 'iOS Test',
                'userName': os.getenv("USER_NAME"),
                'accessKey': os.getenv("ACCESS_KEY")
            }
        }
    else:
        raise ValueError(f"Unsupported platform: {platform}")


def attach_bstack_video(session_id):
    import requests
    bstack_session = requests.get(
    f'https://api.browserstack.com/app-automate/sessions/{session_id}.json',
    auth=(os.getenv('BROWSERSTACK_LOGIN'), os.getenv('BROWSERSTACK_PASS')),
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
    platform = 'android'

    if request.node.get_closest_marker('ios'):
        platform = 'ios'
    elif request.node.get_closest_marker('android'):
        platform = 'android'

    caps = get_capabilities(platform)

    if platform == 'android':
        options = UiAutomator2Options().load_capabilities(caps)
    else:
        options = XCUITestOptions().load_capabilities(caps)

    browser.config.driver_remote_url = os.getenv("BASE_URL")
    browser.config.driver_options = options
    browser.config.timeout = float(os.getenv('timeout', '10.0'))

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

    browser.quit()

    attach_bstack_video(session_id)


def pytest_configure(config):
    config.addinivalue_line("markers", "android: mark test as android only")
    config.addinivalue_line("markers", "ios: mark test as ios only")