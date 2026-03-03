import requests
from datetime import datetime

# ===== 設定 =====
BASE_URL = "https://yoyaku-nishi.growone.net/sportsnet/Welcome.cgi"
MULTISELECT_URL = "https://yoyaku-nishi.growone.net/sportsnet/yoyaku/ShisetsuMultiSelect.cgi"
CALENDAR_URL = "https://yoyaku-nishi.growone.net/sportsnet/yoyaku/CalendarStatusBrowser.cgi"

FACILITY_KEY = "282049_001_17_31_31"  # 甲子園浜（西）

# ===== セッション開始 =====
session = requests.Session()

print("接続開始...")

# ① トップページにアクセス（クッキー取得）
res = session.get(BASE_URL)
res.encoding = "cp932"
print("トップページ取得:", res.status_code)

# ② 施設選択POST
payload1 = {
    "CheckMeisaiUniqKey": FACILITY_KEY
}

res2 = session.post(MULTISELECT_URL, data=payload1)
res2.encoding = "cp932"
print("施設選択POST:", res2.status_code)

# ③ カレンダー取得（今月）
today = datetime.today()
payload2 = {
    "year": today.year,
    "month": today.month
}

res3 = session.post(CALENDAR_URL, data=payload2)
res3.encoding = "cp932"

print("カレンダー取得:", res3.status_code)

# ===== HTMLの一部だけ表示 =====
html = res3.text

print("HTML先頭500文字 ↓")
print(html[:500])

# ===== 空き文字の存在確認 =====
if "○" in html:
    print("空き（○）がHTML内に存在します")
else:
    print("空き（○）は見つかりませんでした")

print("○の出現回数:", html.count("○"))

from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")

# 空き画像を探す
ok_imgs = soup.find_all("img", src=lambda x: x and "icn_scche_ok.png" in x)

print("空きコマ数:", len(ok_imgs))
