# Instagram 貼文照片爬蟲 v2，爬出您鎖定的IG帳號

### 🧰 套件安裝
```ShellSession
$ pip install -r requirements.txt
```

### 💻 執行指令
```ShellSession
$ python3 instagram_crawler.py -s {sessionid_list} -a {account_name} -n {num_post}
```

* `sessionid_list`:自己IG帳號的session_id，如果您有小號，可以自行輸入多組session_id。<br> 
[👉 session id 獲取方式](https://help.captaindata.co/article/112-find-instagram-session-id)

* `account_name`:欲爬取的目標IG帳號名稱

* `num_post`:欲爬取的貼文數(從最新的貼文開始)

* 範例：欲爬取[dcard.tw](https://www.instagram.com/dcard.tw/?hl=en)，前 5 篇貼文的照片<br>
`$ python3 instagram_crawler.py -s {your_sessionid} -a dcard.tw -n 5`


### ❗️ 注意事項
1. 盡量爬公開的帳號
2. 如果要爬不公開的帳號，您自身帳號(session_id)要有追蹤該帳號，否則會爬不到
3. 爬蟲背後原理是使用IG官方 [Graphql API](https://developers.facebook.com/docs/instagram-api/)，爬太頻繁會被鎖住


### ⛔️ 限制
1. 只能夠從第一篇開始爬
2. API 鎖住的頻率變高 from 2022.09.20，所以盡量不要一次爬太多篇，或是要多使用小號(session_id)
