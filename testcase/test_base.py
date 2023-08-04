import os

from api_driver.utils.service_logger import Logger
from api_driver.testcase_mixin import TestcaseMixin


class TestBase(TestcaseMixin):
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    logger = Logger.getLogger("testcase", base_dir)
