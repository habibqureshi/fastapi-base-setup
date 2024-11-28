import logging
import uuid
from fastapi import Depends

from services.current_user_service import get_current_user


def get_logger(currentUser=Depends(get_current_user)):
    logger = logging.getLogger(__name__)
    extra = {
        "currentUser": getattr(currentUser, 'email', "System"),
        "requestId": uuid.uuid4()
    }
    if not logger.hasHandlers():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(currentUser)s %(requestId)s %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    logger = logging.LoggerAdapter(logger, extra)
    return logger
