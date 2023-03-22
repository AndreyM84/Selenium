"""Фикстуры для Firefox"""
import pytest
@pytest.fixture

def firefox_options(firefox_options):
    firefox_options.binary = '/path/to/firefox-bin'
    firefox_options.add_argument('-foreground')
    firefox_options.set_preference('browser.anchor_color', '#FF0000')
    return firefox_options

# firefox_options.binary — путь к exe-драйверу Firefox.
# firefox_options.add_argument(‘-foreground’) — возможность запуска в фоновом или реальном режиме. В нашем случае выбран последний. Для фонового укажите ‘-background’.
# firefox_options.set_preference(‘browser.anchor_color’, ‘#FF0000’) — выбор цвета подложки браузера.


"""Фикстуры для Chrome"""

# import pytest
# @pytest.fixture
def chrome_options(chrome_options):
    chrome_options.binary_location = '/path/to/chrome'
    chrome_options.add_extension('/path/to/extension.crx')
    chrome_options.add_argument('--kiosk')
    return chrome_options

# chrome_options.binary_location — путь к exe браузера (включая сам исполняемый файл).
# chrome_options.add_extension — включение дополнений браузера.

"""Для Chrome существует несколько фикстур, значительно расширяющих работу с драйвером. 
Например, мы можем добавить уровень логирования для более сложных тестовых сценариев (debug):"""

# import pytest
# @pytest.fixture
def driver_args():
    return ['--log-level=LEVEL']

"""Начиная с 59-й версии, Google Chrome стал поставляться с режимом запуска без пользовательского интерфейса, 
с так называемым headless-режимом («без головы»). Это отличный вариант автоматизации для серверов, 
где вам не нужно UI, или оно попросту отсутствует. Например, вы можете запустить несколько тестов 
для настоящей веб-страницы, создать PDF или просто проверить, как браузер отображает страницу.
Мы можем настроить такой режим через фикстуры. Пример кода для использования такой опции:"""

# import pytest
# @pytest.fixture
def chrome_options(chrome_options):
    chrome_options.set_headless(True)
    return chrome_options

# import pytest
import uuid


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep

@pytest.fixture
def web_browser(request, selenium):

    browser = selenium
    browser.set_window_size(1400, 1000)

    # Return browser instance to test case:
    yield browser

    # Do teardown (this code will be executed after each test):

    if request.node.rep_call.failed:
        # Make the screen-shot if test failed:
        try:
            browser.execute_script("document.body.bgColor = 'white';")

            # Make screen-shot for local debug:
            browser.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')

            # For happy debugging:
            print('URL: ', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)

        except:
            pass # just ignore any errors here