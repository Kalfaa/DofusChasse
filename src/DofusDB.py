from enum import Enum
import requests
from unidecode import unidecode
from utils import trouver_chaine_proche 
# Online Python - IDE, Editor, Compiler, Interpreter

class Direction(Enum):
    LEFT=4
    RIGHT=0
    UP=6
    DOWN=2

dict = {"Carapace de tort":"Carapace de tortue","Gravure d'ceil":"Gravure d'œil","Rocher taillé en aretes de poissor":"Rocher taillé en arètes de poisson"}

def comparePos(pos1,pos2):
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

def formatIndice(hint):
    if hint in dict:
        return dict[hint]
    return hint

def get_hints(direction: Direction, position_x: int, position_y: int, hint: str):
    hint = formatIndice(hint.strip())
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'token': '03AFcWeA77RZph1i-lpIZ-P_RSnL9X1zNlV6im_lUVQkP_lD6ipwVm8K07U0s7dniDJQCSilaM11ITkwknT-A2aVFlY3IuXUWxoAGFED4IXmM897xo5pr7mfa0QwXGzvkNKe4z32NB4cknYBXQCYTFs9eY5wGhuF47say38y3Exc_sxD4pGBI5HhTH0US-Afn_ZyEtSCbihms6AfaLbmN4wxVAHIHpmqgQK59o4emA5XFZFXQ3a7LP5JFmSi6CBC4o3wYWliT6JkWnI2DpgcvYL3nZYlbnr3Hb_XZWYefqGrH7FKmqnSBFeQ0Gabn2XHxoJKocnuAnfH5GJyrxWNaYTBYPWJeFJfUiFU1lBK70t8qJzNywIBomvy58fFX7641lpZwX7bOk1G4NZ2I785TGw1XgZFSXOoCZZjYLqHoN7lSC87QWXok8ftvMZZc9UvMMDvQs0gpZeOmIq286RXPz4LlFL6G_hZC5cfm2sHAohq1SNsjGTj7vh0k-PzOh90QQ0sOaiGrCvdCcFiT70Va93oZY8TKRtH-26ZVu6OBhdFKT6KLTUPH67qD0pSUsr4KU0zEGMUuKMPo1OEnlXaiC9sBUFosrkgYfLZJKjCF2LBTEEl8Hd-IqtzSVmYXrUgIAzrcOAZag5VUJbQQ7R_EAScWn2VYxBSRr22LI6AyBFcNZR5MGM7mkeqfZ7o4PwxDHigtxQo6WIGTCxwkenS-hhqtxQPiWGUm3CRBOIM7ms7-n5eGg4ms4KAEejRZ97W0JZTSfnrIsk972EGTMnO8NBDapOlhBQdoNP-ebBAdCBuG-md3VE_NP7zAZ9MTCfd7FfuKg-4WEzQfsgql45TTyqcKQ9sKDUurGIZbcVc6hD5oRQhtLYCzwX9nFE8I6rERhO9f6hId-Bm_tw9CCaaGM1kDuWSZv2QLObLmsLoUZEZrDe04dv7MINSS9TsJi0ZFbmH60ZdUMggllbFhsAjqc6Pmo_4hMXO1U3FKgOBM00Op4I2TkRCIC52Ysi7h042OYifaAgW8W9bav04OUuY-dxivzKSH0whYHgzncKCnugluwb4Zw-5PsrU4mcalCov84SMNXu8yhnDWzrSGLrvB-atpDLQY1t9O6CBZZFz4YzqcSWggKtZnCnG_ydY2LOjMDfovkr14aPQtS9jhuD56Gyju9Wu5U49WcGIZj_mDFb3m-0HDvnR_pUdZd_wWW6DKQf0wnBdko_jfBrAhSaEdxFS1zztPobGLizlgSE3iyo0csqEO886oM5SVUlB4vHv5BksnqYWcyF_kwwS4teuWl80jkYR_R1oLhq3_B4JBgujksw3GJWbt24G9WB5v94emRf3PKt21BM0W5pyI0IlomoLZU7wBKRy3djaWiWHcz7Gj9X1tthGiSy9ohQRQKmh_jfNY_7lg-6MTpblVMlMPKBnMJ-8C_WDQzMFXXyJLYSRx16gxb9VS3AEwoC2Z2w94nU5gNnr-cDC7FPFvT9FG6GZUfhTZN2unAK3cOwRcFb3scdYA9lD1yQnSmfDUeDVzuaGhSp_HH41-_cM8S8mbcKx08W-bliLmTw9aFMuKEpnQO0Ssd49xBVCh2GoSfdgx3094DXvI3nbhGtf-2MhyxFbvJhjr1TNzrcxkeaVlb7dRYeIVxFR1cphpFtVB363-jtAQ4FZZrVROsGxweC8rQmPpayw1spORaLr5Fsg-H9XGN7of2SvrI8lGaL3H-h0LfrXdJaUdg4ok5hxZ9WiY5dilN1_uENS26m5ptwVjfl7LCUNcjWdpTe41ybJmLr2flvU4V7QDoX_gXzxQrWK2WAwL1EV2l4WkE8-klPX0mD_1M681giRYFB0TnoCe8pqqt6ax3NOuFHlOIwCK-hhCKuBtMpXdAr0-pqEGcp6Z-_ghG8IjF9Bo06rVw9-W8lZnVXBNQ2lFgbeLuZIP1xA3rgYK8CEwAh8W2c5ZIExOS61FMDkWFIPlFWQYWkioapq0aoFaYEEGXFJ4xdAkyJx51MCC-GvvD50Um8xux9IMKjlbdFihzhEws3-7kMoPAfBlsH2pShAgsA22mhsfyQtq2oepb1Rdz3A9AjF9z1vXade6405BVZuS5RiQi7LqRZtHbtJwwntjVsv7Lk_xUASiqGC0zmsIEMgpgLvIvLyqMBfWcO8tWYMVGyeMAsGe5X-JwvDSXno0LL0Rk',
        'Origin': 'https://dofusdb.fr',
        'Connection': 'keep-alive',
        'Referer': 'https://dofusdb.fr/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Sec-GPC': '1',
        'Priority': 'u=0',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }
    res = None
    p = 0
    z=position_x
    w='posX'
    if direction == Direction.UP or direction == Direction.DOWN:
        p=1
        z =position_y
        w ='posY'
    hint = trouver_chaine_proche(hint)
    # print(hint)
    print(direction,position_x,position_y,hint)
    req = requests.get(f"https://api.dofusdb.fr/treasure-hunt?x={position_x}&y={position_y}&direction={direction.value}&$limit=50&lang=fr", headers=headers).json()
    # print(req)
    if 'data' not in req:
        return None
    data = req["data"]
    startTuple = (position_x,position_y)
    lastDistance = 1000
    for hints in data:
        for pois in hints["pois"]:
            # print(pois["name"]["fr"])
            if unidecode(hint.lower()).strip() in unidecode(pois["name"]["fr"].lower()).strip():
                # print(hints["posX"], hints["posY"])
                # if res is not None:
                #     # print(res,hints["posX"], hints["posY"])
                #     # print(min(res[p],z),max(res[p],z))
                distance = comparePos(startTuple,(hints["posX"], hints["posY"]))
                if res is None or distance < lastDistance:
                    res = hints["posX"], hints["posY"]
                    lastDistance = distance
    return res