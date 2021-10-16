import requests,json
import _thread,threading
import urllib3
import logging
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import threading, queue
import common
import proxy

def addtocart(productCode):
    addtocart_url = "https://www.ti.com.cn/occservices/v2/ti/addtocart"

    # 添加请求头，需要就传
    header = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "cache-control": "no-store, must-revalidate",
        "content-type": "application/json",
        "expires": "0",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Chromium\";v=\"94\", \"Google Chrome\";v=\"94\", \";Not A Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-sec-clge-req-type": "ajax",
        "referrer": "https://www.ti.com.cn/sitesearch/cn/docs/universalsearch.tsp?langPref=zh-CN&searchTerm=THS6212IRHFT&nr=5",
        "referrerPolicy": "no-referrer-when-downgrade",
        "method": "POST",
        "mode": "cors",
        "cookie": "CONSENTMGR=ts:1632830176853%7Cconsent:true; tiSessionID=017c2c433e580045588fc3c4eb1403078002607000bd0; _ga=GA1.3.1733809788.1632830178; _gcl_au=1.1.1688808738.1632830178; ELOQUA=GUID=443D61824E09450D9A104DFC43A5D3DA; __adroll_fpc=3a7669f09c2d2e7abd89dcdb22696713-1632830265312; user_pref_shipTo=\"CN\"; _fbp=fb.2.1633072810262.713331343; coveo_visitorId=b56afeff-9650-45c5-949f-d6472c282a7f; _gid=GA1.3.1920753731.1634270365; ti_ua=Mozilla%2f5.0%20(Macintosh%3b%20Intel%20Mac%20OS%20X%2010_15_6)%20AppleWebKit%2f537.36%20(KHTML,%20like%20Gecko)%20Chrome%2f94.0.4606.81%20Safari%2f537.36; login-check=null; login-check=null; ti_bm=; __ar_v4=DMF3YWNTG5HTZP5WNBOFAA%3A20210928%3A5%7C3GLIROW56VGDFM2KUHWC42%3A20210928%3A5%7CS4HGNHQ7DNGNJDUXJ2XJA3%3A20210928%3A5%7CG3YHLXUICZC3XKDXYVVLO4%3A20210928%3A14%7C2XNKMR6P4VGD5MD3ZP4SQR%3A20210928%3A14%7CQFXRHQEHOJDMLHSLFIWCLO%3A20210928%3A14%7CIEC2AV647FHDNBUGU23SN7%3A20210929%3A5%7CFJT6BT4YWNEOROP3BJ7ITA%3A20210929%3A5%7C4PSIDGQM4FBWJL6XJJ2EQC%3A20210929%3A6; bm_mi=76D88F5FB73262F209832AB8F8179A30~5ikHhdWj30o/X+8uNpkiRqKmHzGIrzNidp3RjCUWtxn27kX9JwPiqEls07+FLaXcIVg9oTQxiD8V8eFigvUAU+ZEafsJICFmM/di8u96eRMqUq1qsbleKDPt/WX7T3acYxbAxt0GBMM6/kMKYK7cgZGj3xu1Y5b2gkgccn6eNE/xWr0acoGSL3TItWfvsO55ev1rcif239Q+hSHa2j2dIefAlVqnpbLifPdNIMfWMohdMkLwNHRA3YeQpTW3fu0kcxgRF9EuixA9u2WpCkNV6Q==; user_pref_currency=\"CNY\"; user_pref_language=\"zh-CN\"; bm_sz=F149D435198418CD11E51FCF43C3426B~YAAQXQ1x3wNH/VV8AQAAQEvbhw1XiMy6ebjmV7SF4IzrusR03c9HYwJ6IfuURNhXDyWQKc885CrbDEq24NVnzO3em0M2G63jDerhSAMDn9zyaiCOhay3cfPJ1vFYCeqwfnc5kppugVi1mQxFN5YKRipKF9AcDfez2tWIy/GHCMzt2Q/gyjtqu4ePXnZruswyumq682w8etis5duay/kZ6f6I49iSCPjR6Y+8IsYmEhOYfi62fqIa5/Y+TGGGyuuDBt2+9I18Uz39eh8rneRE0Rogzfp6AOwwnkg4//YuRwNDVLklH1I0SSYCI1M8Y0Esq++l+CxP2Gb9UsYI7FvKOTYLUneFDskxNraqlioIoUDGXvDMtIieHxbcc8ohAJseWn755Hc51gVyI2Jps7FXjWlL/EQ=~4277041~4539960; acceleratorSecureGUID=27ae43ace6e195baeccce03a2aff097b4bfc3b3a; ak_bmsc=57F67D4648F8B5AB1C93489212B40EF8~000000000000000000000000000000~YAAQXQ1x3zJK/VV8AQAA4HTbhw1C8+ehsoa0KiYFx0kCce2rooitwBAr4v5KHKj+WSd/S/x9JDPVq3bUZGGvbNNgRiBlH1kJqAreK4/+lJDV4TGIFR8cG8QX/k0QmJQSEca623Z3ZYBz0m4igAWUCJ2NWC5e8HnpvUHyTpYXgB5jlxU0Hzav+LnVdenrpXCWUSXceE0DXeAJKgoQVSl4AGEuTAuynAGEaXEmCc72ItN/FbCiC5RWcZF4TKe46kxHxF5x/D67ZdKtAn0XIdjDasc2zNxnfGwrTWg3COH/UsDyIvkXrx+F20e3Tag0AJXfzIvWNoUXUv+P4Cww+ftCvfL+w8tI90vkPYWIOybUuI2YGE4j62f/h1WpkU/sUjjSk/GMkbjzTYd9Obs0kNccBnNXojt7TN8jrMY8srqrtiKWqsdt5OBQ9yu2MJv2AlSfP9+M3G/x+GZuccr6icg1nnn3rB9H7ZU=; user_pref_givenName=\"%E8%94%A1\"; user_pref_givenNameLocalLanguage=\"%E8%94%A1\"; ti_geo=country=CN|city=SHANGHAI|continent=AS|tc_ip=117.144.47.226; user_pref_permanentId=\"6822002\"; user_pref_uid=\"scnu_xiaokun@qq.com\"; last-domain=www.ti.com.cn; tipage=%2Fsitesearch%2Fcn%2Fdocs%2F%E6%90%9C%E7%B4%A2%E7%BB%93%E6%9E%9C; tipageshort=%E6%90%9C%E7%B4%A2%E7%BB%93%E6%9E%9C; ticontent=%2Fsitesearch%2Fcn%2Fdocs; ga_page_cookie=%E6%90%9C%E7%B4%A2%E7%BB%93%E6%9E%9C; ga_content_cookie=%2Fsitesearch%2Fcn%2Fdocs; ABTasty=uid=j6wshax2z59xfgv8&fst=1632830177486&pst=1634308134253&cst=1634366860009&ns=26&pvt=224&pvis=13&th=686831.851794.175.13.20.1.1632830480571.1634368587821.1_759046.943435.6.6.1.1.1632907981896.1632924253873.1; ABTastySession=mrasn=&sen=25&lp=https%253A%252F%252Fwww.ti.com.cn%252F; da_sid=5C752F108E32AE92E47FAA1348D1A57F62|3|0|3; da_lid=6F461C239A72EA2BDA16BB990A787153DA|0|0|0; da_intState=; auth_session=glQCVABlhdgiKPD9.cdfsNksME3PczdfqEzjevzFPyptTKvAHE7NgqmJAq0JoN7hhGsal5FrzVNwI9G1mFk-xft5B_t8y2RUwsqg4qAFXVoKXIF9Yymc2wgsq9Agfb9jf8wuhaR6WOaDqc8yEBXCxCWR3wU_uC6S5qmcEyAu3add0FTdQ0ghO7Saff8075aQUmTOEhYBp6fdg58IAFKPZ5yruCdZCrGr4AdOPOPJqwcU9ccbz5i3twazIOnZfbHy9Yc3mKojNQjq8BSShWxLI8_1l_hot50EMuN_NamR19hmngiDFJDj7OrdB9-byEumYRO1qlLNYKhIZBIj5mI3yLvNCYAinSu6T6pKa7BW0K-Y07rW6tMD9fhKJVz1zXYeTemUcr50jZlNjaLWyridRj6OKtX6z0nGWVKUXeP8HvQbCrP0806RRrus2tiRmz7Xtoh5mHEHdp8qwPYlJLbng1qDyxOyZhaC8nhlxI-xYXB6tJuDRDwK7zgOYcuLjsnnSE2Hn0LmZxUKGbbuDyJGcJk6L9CrZXgnPlgrnzPPPdTlGr7oEll5lSHQ2uEUERhr_s9JaR1UUpseu8a6MZUnZveJAcy0yO1maCBsYmLUTk80v7AvtruEVgvy1iqyj1jFkHtHeaXN8kiU9BNPHy116NMmpIDV3M2lTy-t4-L00bLHLoPeVxl5f2pAYcGqLrhQeTxxrYILj1FAFiUezP5_PgPB5laTMdUsgrpBqRXwcs2nRsezbRgukAhxjg917VuMCl4rC2xQSA4Z69adKXH2BwwydNvFlfcxJ8sHeoaawYd72RbDMhtVw3m97U6KLnmQvXjUjVlFHCtk3PTzrtFeeR6UYyqtBxItLbiDPT7RJ0RH2tAlpPsy_hP7rJ-xMIW6UCcnZzfXltfAR7P3ByLL7p8bjUaJXAVagOeEsrtUte32mbbd3Esg8cdgtNrvl6IowPEQ08kma9qk_Ul8YifcmKFUELKRxb9HF_YR4XOO0P9nvOJ_riqMJJWx0aRf6Vrv7F9acyUXLEs__ysDvbtbwOsg16Bs78Lh0BO-c2JrhByiG4nhxlXbpn1_waCJA_a3Pui3c3Mb46krAXH0PdOhUCpZV6ThLOF31oAQOsrx1c6psv6agGPvuj1A7q8pqdYSQZwDx8VUEt81pUvRtf4ddBru6WUsL8GRSNMLNbDZfb4qKjBvsquHHOIwYiTqcxkIoY8P8UEFTfrab13lenuM-Dop1Bx2kv-qsMZkdKDyrw_xrs_lZwF5cGNt2h0Au-OqdqMsdJZEZ5oz9XvBfwbBnQQ9aoM3WhmN1am3rKVk5NwJ9Pvl1mOW-rq_Sl9ieBYyK47OOil1qeNMXdC44igufqAHRr543VvY7zYL2tPxwk8N0wh1dk8UHieduQ65pM3wXS99YkfvDbx5ZsD3TxzDcVfMA3a4FL2QrGV3AkOiE-JZ_60bgkiNFNBuzczMUVrraHsPdAT2dgJZLCcLE7NuSE4UCaQ--7SO8UohRbiQRqqDvgTVYzfO9TkM-z0xFsC416a-Tygov4UbvcJ6RwVuh3Jb5dUseb-03-gEVyKg5mT6AvEbH6Bddh4UPrritTQwKhcPo15tlnDOi3doSAcYtohjCSI18mc9jd7EhSqx43nbPwuxBGPymktrGMRu0MLvsZMTJ.IM1HiiXTIEKGNfKwrjE6pQ; userType=Anonymous; _gat_ga_main_tracker=1; utag_main=v_id:017c2c433e580045588fc3c4eb1403078002607000bd0$_sn:25$_ss:0$_st:1634371179284$free_trial:false$dc_visit:13$_pn:13%3Bexp-session$ses_id:1634366859217%3Bexp-session$dc_event:15%3Bexp-session$dc_region:ap-northeast-1%3Bexp-session; ti_rid=ed86b93; bm_sv=7CB6B81FA5B03484F593E3FE264F7025~OuDz/bGMYt3HHuTCm/Zg2yecMlfh+BGSXbcfRgQaXb9ZMdONGOxdyhDZby9ZqU7Wf6qOdposmXfIB1ocf+38j5X1ViJOHE53om60STqcWs4VXBJjmfrIGUJBn3sQAwLwW4zHSrRRxq1yWZIVljQDLnKFAZ5cWEGrUHB+5/Ke1ZY=; _abck=D98E4E551CDCA02D2A26334F85012BB5~-1~YAAQHFCcJE2nMlh8AQAA46ABiAZmRnIfubfm5KttqgCubUZ3vlChyvd/Qc0H0j86RGuD4y5H/fzSmzXmP9ko8Z/R7TXNuDHlnbh2PpptYlhr4wgZvG867tpfSyGkfXY1/d39lymHyqTB3G+jsp7pT732hpsVcCWd+Zb5nAhnv83R/zqdfrb6S5Scm3LnONMEydvbr2y9W+dfNDpwlvXyE+AhdOrc2M/gnalfPUsO1tBEGkcjZ59CXKgnSl6FY2vd4cQqXjbO6z8YF22pcsQaZ1C8dNF1DOXuupZNGek89DoWSpH4tWQlyePXS2r3rSFr83h6EfWO9E42Y8+PfqpDF12YL4fcg+8tbY0JCMj8cju/HI8BhOso0ZuHgZ2dtAj2pG3A2QAVrvEIMTHM2r2jGIl4CaMerT3cQ17+/gPoYiqlie4rK3JiTjVIqa2I/U0Kw1zzimb8/iQy4eogWaXq9efAPqI=~-1~-1~-1"
    }

    # json类型的参数
    payload = {
        "cartRequestList": [
            {
                "packageOption": "CTX",
                "opnId": "THS6212IRHFT",
                "quantity": "1",
                "tiAddtoCartSource": "ti.com-opnsearch",
                "sparam": ""
            }
        ],
        "currency": "CNY"
    }

    response = requests.post(url=addtocart_url, json=payload, headers=header)
    # logger.info(response.text)
    return response

# logger = common.initLoger()
# if __name__ == '__main__':
#     logger.info('==================PyCharm Start====================')
#
#     # loopProductListToGetInventoryV2()
#     # autoBuyProductByCodeV2("BQ29209", ["BQ29209DRBR"])
#     # autoBuyProductByCode("BQ7692000PWR")
#
#     # 通过url直接加上请求参数，与通过params传参效果是一样的
#
#     response =addtocart("THS6212IRHFT")
#     logger.info(response.status_code)
#     logger.info(response.text)
#     logger.info('==================PyCharm End====================')