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
default_token = '03AFcWeA6iVVcyc97jIGreGqubFfVWwHGzGEbmnn1wD4bA0zWqDcWqeOdcXz-xBdKdAfqqp344LH1iGtWKHeBdraOpPKLNvTdYzyyGIHACYVEhzbyu-A6k77_ws-a2n45Rw4tLTHTiIdrcwGC2Gd5y0Mtg93rvx7DSA5UbO1Ll0z3MtlULHjHSiMlcgfS08bW7ivPOLU7yW__9zPnAQqPtzPhLvoijQcyTVU-hJw255AhP4p9RlZvMV2gBCQkYG3Hm3qwNtd8_oj4ufP4Ts4oSppFuAcH0M_PhP1Jkh1uigAfD1lNm4Zb7FCpyPLQLg72RfHwZFJvwxjtAWZjcIG1JcQEJora3xIv-OPsJiSstkiHbA-AKPhrSS8JOH5ApTss5SM08hGhgK4HFOIkr9TSs0KZ8ecMVvUNHnYwH4Se3SJhmfGZUN2voTlu1ejq61JAaIgoZilWhSWQ0N9KwSQ6KAG6Nu4_l0_kMHZAAm53lfLbqJ-V-RIA8ejbyRr_D47Q8oK9iCDfbqn6VTyEb3zBg5YH-pn7KfixGh3Ul2qbSHK52E62pc548seP2wvCZCj6B4_C9wwA_0Sgp5hnTLGArxIWySlXSF9J-4nKfwsmvEN67ebhsBYapUdxPRwvZ1dVSjK6AFPCBbV5BPbR-KItWtwMh177-CnEefN6lcT9Ssdsr7g_Dr--04e9fQF5WqymLEOFPbf9Q9V2-7EWpSQFjdrE8UpCO43qpthw1j4oc9JdfWuOaYVB5UxLg2rOHz7Jll3huJRJlkUfZ8X_VkjXqRAlHO_jcCg-2jKD3tmPZ6KANDMW94nHK1vuU5hFtIbMsGV3qrLPLKPBOmJo_JfGGgGItNEw1P5CPdR3uI0rqnXDIdzI79g3xX8xKDfz4df3IKmzAWTXnTzIspDFz4eeCpNJJd2-lzAAqNGqPtCLV5yxOR2FQcbc-fRwHZ_nZIes4cZfEaexeXg-J3TypwkPZZd-yi6ENxa6to1V9duCVTgTHZL1kTOP_zVYZm0J1J8By68Hbtm86EPvFBdMGgWQnRKAD2qYNqkuxSx1YcfY_-Nl7dBb1OSqvnqWKjMVxk8E2wlFSkWlNj0wQdhUXsEOjbjWr2xmNkKxv_FuDJdvCjVIdRcbHq2p1yfXxfH-N-oCala3rCoskzbJCF7eMEdXGRXijevZ_qPLiVnZlkWjVUIOdvITcEB9dwUvckeolpBbekua4QmPdwVoNqg4bihbyA8avh82jCOhathqUSZPw1CKIU5wlVp4XHIV0ymHYd_vRR59AXnHUaErGc9tiytB51nvZ1eDTi1gbix1hf4CsB6jezeZ87OI5esA6bBY_X96I-dn_FGjprmUyXFNm11aJvo7cbArbFFkyXkcCD0i7mINQr7ocEFrzRYSMLbkN8kSEnqjXaj6hipR5p_aZ2QK5capGYkyIEzCFRTad0nLEAuFWcYQ2tdIggoptJvI271YX31leOh4g2vuYOu5TPzK-1X5c-xUQRFMhRe_Wvm29XrtWC2iW4NCoidvCEr6VhcXSU537qh9Xcx4VBIz_8YY63qkUFOYx_Z0cLyzjHU0OQjXbQXR5_DdkwFcAmw1Q5-NZNgxHM2gWjHtVQFTyz77PpHtd5sI5RGNGH04BktM9X7sQo6BPsS5v68nP-741G4ZxrMEWkvIgosOEP4HLwfq61hWaAN973YJiEwuD_0xPmHcmn-BYyJu0F9RpCXIuMwmtrJyxFBO4zZNmI_AG1CSgpFPNFmgz3-HQXWV0Cs69TyZUzoqCJbRySBdw08_fR3zOHCAJzeAOkOLGf8GsWqn9b9Fc1pIFCA9mxbMtoa60zIv9e9A2KOGiA5VORDO4433oo0LdBBLYYaL0nQA8Rp7B08XDVNT5lJlzMHNoQgkhuyw6XrWiEcm9e28UFFYUkaj8PYFJB9bgbMusSLn1rMBIqDqPwSFwk9Eb-MiStWeFvJOUwyYXFo7iqHBU9QWTDbDbJZj98xuHByKhVa6l_cfRskx-kKnAZ-yyhzJTL7Mm81lIBp-ZpnEcjUNLgaJR_XVPFlGoh7talZM3r7KWT0QHXp4lW8JqZn8cuw1T20ESr1Kpccel4l1aEwTcmzYx1XGfxVnOTXEaeFo3K_cxAnpuB8UeJnLN7S2Fm0Er3tv2jYiQfofTDOCWz5IE3eKAd6kUr_6AXFZFd_5p'
dict = {"Carapace de tort":"Carapace de tortue","Gravure d'ceil":"Gravure d'œil","Rocher taillé en aretes de poissor":"Rocher taillé en arètes de poisson"}

def comparePos(pos1,pos2):
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

def formatIndice(hint):
    if hint in dict:
        return dict[hint]
    return hint

def get_hints(direction: Direction, position_x: int, position_y: int, hint: str, token: str = default_token):
    print("bonjour")
    hint = formatIndice(hint.strip())
    print("token", token.get())
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'token': token.get(),
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
    print("just did the call")
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