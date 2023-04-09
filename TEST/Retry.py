import time

from retrying import retry
import MyUtils
import selenium

index = 0


@retry(retry_on_exception=MyUtils.retry)
def main():
    time.sleep(3)
    exit(-1)
    raise selenium.common.exceptions.TimeoutException


if __name__ == '__main__':
    main()
