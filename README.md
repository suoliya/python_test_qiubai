# python_test_qiubai
练手用python写了一个糗百的爬虫小脚本，用mysql，直接存库，没有用线程
需要用到的模块
import re
import time
import requests
import pandas as pd
from retrying import retry
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import pymysql
