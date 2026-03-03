import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ===== URL設定（自分のURLに置き換えて）=====
BASE_URL = "https://yoyaku-nishi.growone.net/sportsnet/Welcome.cgi"
MULTISELECT_URL = "https://yoyaku-nishi.growone.net/sportsnet/yoyaku/ShisetsuMultiSelect.cgi"
CALENDAR_URL = "https://yoyaku-nishi.growone.net/sportsnet/yoyaku/CalendarStatusBrowser.cgi"

# ===== 監視対象施設 =====
FACILITIES = {
    "塩瀬中央公園": "282049_001_15_31_31",
    "西宮浜総合公園北_A": "282049_001_16_31_31",
    "西宮浜総合公園北_B": "282049_001_16_32_32",
    "西宮浜総合公園北_C": "282049_001_16_33_33",
    "甲子園浜海浜公園（西）": "282049_001_17_31_31",
}

def check_facility(name, key):

    session = requests.Session()

    # ① トップページ
    res = session.get(BASE_URL)
    res.encoding = "cp932"

    # ② 施設選択
    payload1 = {
        "CheckMeisaiUniqKey": key
    }
    res2 = session.post(MULTISELECT_URL, data=payload1)
    res2.encoding = "cp932"

    # ③ カレンダー取得（今月）
    today = datetime.today()
    payload2 = {
        "year": today.year,
        "month": today.month
    }

    res3 = session.post(CALENDAR_URL, data=payload2)
    res3.encoding = "cp932"

    html = res3.text

    soup = BeautifulSoup(html, "html.parser")

    # 空き画像を探す
    ok_imgs = soup.find_all("img", src=lambda x: x and "icn_scche_ok.png" in x)

    return len(ok_imgs)


# ===== 全施設チェック =====
print("===== 全施設空きチェック開始 =====")

for name, key in FACILITIES.items():
    try:
        count = check_facility(name, key)
        print(f"{name} → 空きコマ数: {count}")
    except Exception as e:
        print(f"{name} → エラー: {e}")

print("===== チェック終了 =====")
