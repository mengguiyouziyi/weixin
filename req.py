import requests

url = "https://mp.weixin.qq.com/profile"

querystring = {"src": "3", "timestamp": "1504663136", "ver": "1",
               "signature": "O77UQkrCAZayi0Nv2RrNZ6Chr0C2SYiF9K47s6rbJdBLqZXR6evuShH9iuU-5WnjEHwPd52*DPmfTOe3mDvYLg=="}

headers = {
	'upgrade-insecure-requests': "1",
	'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
	'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	'accept-encoding': "gzip, deflate, br",
	'accept-language': "zh-CN,zh;q=0.8",
	'cookie': "RK=mANPtD8eQR; pgv_pvi=7332012032; sd_userid=54101497259025450; sd_cookie_crttime=1497259025450; tvfe_boss_uuid=2df455c17b493681; ptui_loginuin=1054542506; _qpsvr_localtk=tk6262; pac_uid=1_775618369; ptcz=373bd6a23bc86488efcf835f7b525ab131e8b91a6a31139a4634e4593b1cbf8c; pt2gguin=o0775618369; pgv_pvid=9631912360; o_cookie=775618369; sig=h01b0f9ff53999c3eb5082cdb4b6f4392ab2cb701e1e973d2439a3450bd2e568bc1cc85d3013c72db53",
	'cache-control': "no-cache",
	'postman-token': "c2ed11f2-dff8-8443-b281-dbe70a2309c8"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
