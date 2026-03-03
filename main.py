import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ====== URL設定（自分のURLに必ず置き換える）======
BASE_URL = "https://yoyaku-nishi.growone.net/sportsnet/Welcome.cgi"
MULTISELECT_URL = "https://yoyaku-nishi.growone.net/sportsnet/yoyaku/ShisetsuMultiSelect.cgi"
CALENDAR_URL = "https://yoyaku-nishi.growone.net/sportsnet/yoyaku/CalendarStatusBrowser.cgi"

# ====== 監視対象施設 ======
FACILITIES = {
    "塩瀬中央公園": "282049_001_15_31_31",
    "西宮浜総合公園北_A": "282049_001_16_31_31",
    "西宮浜総合公園北_B": "282049_001_16_32_32",
    "西宮浜総合公園北_C": "282049_001_16_33_33",
    "甲子園浜海浜公園（西）": "282049_001_17_31_31",
}


def check_facility(name, key):

    session = requests.Session()

    print("-----", name, "-----")

    # ① トップページGET
    res = session.get(BASE_URL)
    res.encoding = "cp932"

    # hidden取得
    soup_top = BeautifulSoup(res.text, "html.parser")
    hidden_inputs = soup_top.find_all("input", type="hidden")

    payload1 = {}
    for h in hidden_inputs:
        if h.get("name"):
            payload1[h.get("name")] = h.get("value", "")

    # 施設キー追加
    payload1["CheckMeisaiUniqKey"] = key

    # ② 施設選択POST
    res2 = session.post(MULTISELECT_URL, data=payload1)
    res2.encoding = "cp932"

    print("施設選択後HTML長さ:", len(res2.text))

    # セッションエラー判定
    if "セッションエラー" in res2.text:
        print("⚠ セッションエラー発生")
        return 0

    # ③ カレンダー取得（今月）
    today = datetime.today()

    payload2 = {}
    soup_after = BeautifulSoup(res2.text, "html.parser")
    hidden2 = soup_after.find_all("input", type="hidden")

    for h in hidden2:
        if h.get("name"):
            payload2[h.get("name")] = h.get("value", "")

    payload2["year"] = today.year
    payload2["month"] = today.month

    res3 = session.post(CALENDAR_URL, data=payload2)
    res3.encoding = "cp932"

    html = res3.text
    soup = BeautifulSoup(html, "html.parser")

    # デバッグ：thの数確認
    th_count = len(soup.find_all("th"))
    print("th（日付列）数:", th_count)

    # 空き画像探し
    ok_imgs = soup.find_all("img", src=lambda x: x and "icn_scche_ok.png" in x)

    return len(ok_imgs)


# ====== 実行 ======
print("===== 全施設空きチェック開始 =====")

for name, key in FACILITIES.items():
    try:
        count = check_facility(name, key)
        print(name, "→ 空きコマ数:", count)
    except Exception as e:
        print(name, "→ エラー:", e)

print("===== チェック終了 =====")
