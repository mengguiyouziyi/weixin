import requests

url = "https://c.liepin.com/connection/loadattention-b.json"

payload = {'userh_ids': 8263938}
headers = {
	'accept': "application/json, text/javascript, */*; q=0.01",
	'origin': "https://c.liepin.com",
	'x-requested-with': "XMLHttpRequest",
	'x-alt-referer': "https://www.liepin.com/company/8263938/",
	'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
	'content-type': "application/x-www-form-urlencoded",
	'referer': "https://c.liepin.com/ajaxproxy.html",
	'accept-encoding': "gzip, deflate, br",
	'accept-language': "zh-CN,zh;q=0.8",
	'cookie': "__uuid=1497169597459.78; _uuid=9643208EFFA8420B2E3819BF1123A588; user_kind=0; is_lp_user=true; gr_user_id=0ebb5885-4510-46ae-91a3-a8f8fa68b3c9; fe_all_activetab=contacts; _fecdn_=1; abtest=0; gr_session_id_bad1b2d9162fab1f80dde1897f7a2972=12d66ef0-aafc-4adb-b889-f0cef0a04a94; __tlog=1506508854863.59%7C00000000%7C00000000%7Cs_o_001%7Cs_o_001; __session_seq=3; __uv_seq=2; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1509594812; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1509594824",
	'cache-control': "no-cache",
	'postman-token': "cd88cb3e-a143-6573-5662-2cfff5afe2da"
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
