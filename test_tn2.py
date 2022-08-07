import logging
from en_norm import tts_norm

logging.basicConfig(filename = 'testinfo.log', level = logging.INFO, format = '%(asctime)s:%(levelname)s:%(message)s')
# logging.basicConfig(filename = 'testerror.log', level = logging.ERROR, format = '%(asctime)s:%(levelname)s:%(message)s')

f = open("test_tn2.txt", "r")
lines = f.readlines()
 #testing currency
def test_1():
    try:
    # only two items in a row
        for line in lines:
            t1, a1 = line.split("|")
            assert(tts_norm(t1.strip())==a1.strip())
    except AssertionError as err:
        logging.info(t1 + " -> " + a1)
test_1()