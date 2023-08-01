import re

from django.test import TestCase


# Create your tests here.


res = re.search('_(.*)?_', 'test_4_1689041837.py')
print(res.group(1))
