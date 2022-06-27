import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--start_day', type=str, default = "2019-12-19", help='crawling start day')
parser.add_argument('--end_day', type=str, default = "2019-12-22", help='crawling end day')
parser.add_argument('--url', type=str, default = "https://www.bigkinds.or.kr/", help='Bigkinds url')
parser.add_argument('--click_time', type=float, default = 1.5, help='click time')
parser.add_argument('--send_time', type=float, default = 0.5, help='click time')
parser.add_argument('--date_time', type=float, default = 2, help='date time')
parser.add_argument('--wait_time', type=float, default = 10, help='wait time')
parser.add_argument('--driver_path', type=str, default = 'C:/Users/COMG/programming/GodsToImage/scrap/chromedriver_win32/chromedriver.exe', help='Chrome driver execution path')


