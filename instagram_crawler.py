import urllib
import urllib.request as req
import os, time, sys, requests, json, random ,bs4, re
from datetime import datetime, timedelta
import pandas as pd
import argparse

class ig_photo_crawler():
    def __init__(self, session_id, target_account, num_post):
        self.ta_account = target_account
        self.sid = session_id
        self.agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
        if num_post<100:
            self.first = str(num_post)
        else:
            self.first = "100"
        self.num_post = num_post
        
    def get_ig_id(self, acct_name):
        url = f"https://www.instagram.com/{acct_name}?__a=1"
        print(url)
        headers = {"user-agent":self.agent,"cookie":"sessionid=%s"}
        headers['cookie'] = headers['cookie'] % self.sid[random.randrange(0,len(self.sid))]
        print(headers['cookie'])
        Url = req.Request(url, headers=headers)
        with req.urlopen(Url) as response:
            data = response.read().decode("utf-8")
        soup = bs4.BeautifulSoup(data, "html.parser")
        js = json.loads(soup.text)
        ig_id = re.search('(?<=profilePage_).*', js['logging_page_id'], re.IGNORECASE).group(0)
        return ig_id

    def get_all_post_shortcodes(self, ig_id):
        shortcode_list = []
        has_next_page = False
        post_remained = self.num_post
        while True:
            variables = {"id":ig_id, "first":self.first}
            if has_next_page:
                variables['after'] = end_cursor
            # varibles['after'] = js['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
            variables = json.dumps(variables, separators=(',', ':'))
            profile_url = "https://www.instagram.com/graphql/query/?query_hash=472f257a40c653c64c666ce877d59d2b&variables=%s"
            print(urllib.parse.quote(variables))

            url = profile_url % urllib.parse.quote(variables)
            print(url)

            # ????????????????????????...????????????
            headers = {"user-agent":self.agent,"cookie":"sessionid=%s"}
            headers['cookie'] = headers['cookie'] % self.sid[random.randrange(0,len(self.sid))]
            print(headers['cookie'])
            Url = req.Request(url, headers=headers)
            with req.urlopen(Url) as response:
                data = response.read().decode("utf-8")
            soup = bs4.BeautifulSoup(data, "html.parser")
            js = json.loads(soup.string)
            # ???????????????????????????????????????????????????????????????
            has_next_page = js['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
            end_cursor = js['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']

            len_post = len(js['data']['user']['edge_owner_to_timeline_media']['edges'])
            post_remained -= 100
            print(f"??????profile??????????????????{len_post}")
            for i in range(0, len_post):
                js['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']
                short_code = js['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['shortcode']
                print(short_code)
                shortcode_list.append(short_code)

            if has_next_page==False:
                break
            elif post_remained<0:
                break
            print("time sleeping...")
            time.sleep(random.randrange(10,20))
        return shortcode_list

    def get_photo_urls_from_shortcodes(self, shortcodes):
        shortcode_photo_url_pairs = []
        for new_sc in shortcodes:
            url = f"https://www.instagram.com/p/{new_sc}?__a=1"
            print(url)
            headers = {"user-agent":self.agent,"cookie":"sessionid=%s"}
            headers['cookie'] = headers['cookie'] % self.sid[random.randrange(0,len(self.sid))] #?????????sessionid
            print(headers['cookie'])
            Url = req.Request(url, headers=headers)
            with req.urlopen(Url) as response:
                data = response.read().decode("utf-8")
            soup = bs4.BeautifulSoup(data, "html.parser")
            js = json.loads(soup.text)

            if 'edge_sidecar_to_children' in js['graphql']['shortcode_media'].keys():
                #????????????????????????
                for sub_po in js['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']:
                    display_url = sub_po['node']['display_url']
                    shortcode_photo_url_pairs.append({'short_code':new_sc, 'display_url':display_url})
            else:
                display_url = js['graphql']['shortcode_media']['display_url']
                shortcode_photo_url_pairs.append({'short_code':new_sc, 'display_url':display_url})
            #break
            print("time sleeping...")
            time.sleep(random.randrange(10,30))
        return shortcode_photo_url_pairs

    def download_photo(self, shortcode_photo_pairs):
        os.mkdir(self.ta_account)
        i = 0
        for ele in shortcode_photo_pairs:
            file_name = f"./{self.ta_account}/"+ele['short_code']+f'{i}.jpg'
            print(file_name)
            req.urlretrieve(ele['display_url'], file_name)
            print("time sleeping...")
            time.sleep(random.randrange(3,5))
            i = i+1 #?????????shotcode???????????????
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="??????ig account session_id(???????????????)", type=str, nargs='+', required=True)
    parser.add_argument("-a", help="????????????????????? ig account", type=str, nargs=1, required=True)
    parser.add_argument("-n", help="????????????????????? ?????????", type=int, nargs=1, required=True)
    args = parser.parse_args()
    # print(type(args.n[0]))

    igc_op = ig_photo_crawler(session_id=args.s, target_account=args.a[0], num_post=args.n[0])
    print("getting target ig_id")
    target_ig_id = igc_op.get_ig_id(acct_name=igc_op.ta_account)
    print(target_ig_id)

    print("getting post shortcodes")
    shortcode_list = igc_op.get_all_post_shortcodes(ig_id=target_ig_id)
    print(shortcode_list)

    print("getting shortcodes and photo_url dict")
    sc_photo_pairs = igc_op.get_photo_urls_from_shortcodes(shortcodes=shortcode_list)

    print("start downloading all photos")
    igc_op.download_photo(shortcode_photo_pairs=sc_photo_pairs)

    print("scrapping done")

    os._exit(0)