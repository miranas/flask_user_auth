import logging

logging.basicConfig(
    filename= 'access_log.txt',
    level = logging.INFO,
    format = '%(asctime)s: %(levelname)s %(message)s'
    
)