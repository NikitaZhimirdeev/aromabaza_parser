import requests
from sel

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}

def main():
    pr = {
        'https': 'http://168.235.69.34:80'
    }
    r = requests.get('https://www.bestbuy.com/', proxies={'https': f'http://168.235.69.34:80'})

    print(r.text)

if __name__ == '__main__':
    main()