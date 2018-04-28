import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S', filename='test.log', filemode='w')

logger = logging.getLogger(__name__)
logging.debug('this is debug message')
logging.info('this is info message')
logging.warning('this is warning message')