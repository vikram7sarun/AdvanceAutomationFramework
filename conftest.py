from venv import logger

import pytest
import logging
from datetime import datetime
from config.config import Config
import yaml
from selenium import webdriver
from base.webdriverfactory import WebDriverFactory

@pytest.fixture(scope="class")
def setup(request):
    browser = request.config.getoption("--browser").lower()
    remote = request.config.getoption("--remote")
    wdf = WebDriverFactory(browser, remote)
    driver = wdf.getWebDriverInstance()
    if request.cls is not None:
        request.cls.driver = driver
    yield driver
    driver.quit()


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser to run tests on (chrome, firefox, edge)")
    parser.addoption("--remote", default="http://localhost:4444/wd/hub")


def setup_logger():
    """Configure logger settings."""
    logger = logging.getLogger("TestLogger")
    logger.setLevel(logging.DEBUG)

    # Create a file handler to store logs with a timestamped filename
    log_filename = f"logs/test_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler for console output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Set a format for log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logstart(nodeid, location):
    """Log the start of each test."""
    logger.info(f"Starting test: {nodeid}")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logfinish(nodeid, location):
    """Log the end of each test."""
    logger.info(f"Finished test: {nodeid}")






