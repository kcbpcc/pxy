import requests
from bs4 import BeautifulSoup
import traceback

class Trendlyne:
    base_url = "https://trendlyne.com/"
    entry_url = base_url + "fundamentals/stock-screener/432332/buy-plus-pxy/"
    
    def __init__(self):
        fake_response = requests.get(self.base_url)
        fake_cookies = fake_response.cookies
        csrf_token = fake_cookies.get('csrftoken')
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "Referer": self.base_url,
            "Cookie": "csrftoken={}".format(csrf_token),
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site"
        }

    def entry(self):
        try:
            r = requests.get(self.entry_url, headers=self.headers)
            r.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            
            soup = BeautifulSoup(r.content, 'html.parser')
            
            maintag = soup.find(name='main')
            if maintag is not None:
                tbody = maintag.find(name='tbody')
                if tbody is not None:
                    data_list = tbody.find_all(name='span', attrs={'class': 'column-value'})
                    inner_contents = [span.get_text(strip=True).replace('%', '') for span in data_list]
                    inner_contents = [content.replace('\n', '').replace(' ', '') for content in inner_contents]
                    rows = [inner_contents[i:i+9] for i in range(0, len(inner_contents), 9)]

                    data_list_of_dicts = []
                    for row in rows:
                        data_dict = {
                            'power': row[0],
                            'tradingsymbol': row[1],
                            'QTY': row[2],
                            '4': row[3],
                            '5': row[4],
                            '6': row[5],
                            '7': row[6],
                            '8': row[7],
                            '9': row[8]
                        }
                        data_list_of_dicts.append(data_dict)
                    print(data_list_of_dicts)
                else:
                    print("No 'tbody' element found on the page.")
            else:
                print("No 'main' element found on the page.")
        except requests.exceptions.RequestException as req_err:
            print(f"Request failed: {req_err}")
        except Exception as e:
            print(f"An error occurred: {e}")
            print(traceback.format_exc())

if __name__ == '__main__':
    t = Trendlyne()
    t.entry()
