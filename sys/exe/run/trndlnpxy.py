import requests
from bs4 import BeautifulSoup
import traceback
from utcpxy import peak_time
peak = peak_time()

class Trendlyne:

    base_url = "https://trendlyne.com/"
    nonpeakurl = base_url + "fundamentals/v1/stock-screener/432332/buy-plus-pxy/all/all/" 
    peakendurl = base_url + "fundamentals/v1/stock-screener/432332/buy-plus-pxy/all/all/" 
    entry_url = peakendurl if peak == 'PEAKEND' else nonpeakurl

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
            if r.status_code == 200:
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
                                '0': row[0],
                                'tradingsymbol': row[1],
                                'QTY': row[2],
                                '4': row[3],
                                '5': row[4],
                                '6': row[5],
                                '7': row[6],
                                '8': row[7]
                            }
                            data_list_of_dicts.append(data_dict)
                        return data_list_of_dicts
                    else:
                        print("No 'tbody' element found on the page.")
                else:
                    print("No 'main' element found on the page.")
            else:
                print("Request failed with status code:", r.status_code)
        except Exception as e:
            print(traceback.format_exc())
            print(e)

if __name__ == '__main__':
    t = Trendlyne()
    print(t.entry())
