# Instagram 貼文照片爬蟲V2，爬出您鎖定的IG帳號

### 🧰 套件安裝

### 💻 執行指令
```
$ python3 instagram_crawler.py -s {sessionid_list} -a {account_name} -n {num_post}
```

* `sessionid_list`:自己IG帳號的session_id，如果您有小號，可以自行輸入多組session_id。[👉session id 獲取方式](https://help.captaindata.co/article/112-find-instagram-session-id)

* `account_name`:欲爬取的目標IG帳號名稱

* `num_post`:欲爬取的貼文數(從最新的貼文開始)

* 範例：欲爬取[dcard.tw](https://www.instagram.com/dcard.tw/?hl=en)，前 10 篇貼文的照片 <br>
`$ python3 instagram_crawler.py -s {my_sessionid} -a dcard.tw -n 10`


### ❗️ 注意事項
1. 盡量爬公開的帳號
2. 如果要爬不公開的帳號，您自身帳號(session_id)要有追蹤該帳號，否則會爬不到
