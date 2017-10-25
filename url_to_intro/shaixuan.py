import codecs
import base64

file_list = ['gzhUrl_bj_1015_1.log', 'gzhUrl_bj_1015_2.log', 'gzhUrl_bj_1015_3.log', 'gzhUrl_bj_1015_4.log',
             'gzhUrl_sh_1015_1.log', 'gzhUrl_sh_1015_2.log', 'gzhUrl_sh_1015_3.log']
# path_list = ['public_num.log']
jishu = 0
quchong = set()
for name in file_list:
	with codecs.open('weixin_quchong_all.log', 'a', 'cp1252') as file:
		with codecs.open(name, 'r', 'cp1252') as f:
			for line in f:
				biz_b = line[:16]
				url = line[17:]
				if not url.startswith('http'):
					continue
				biz_str = base64.urlsafe_b64decode(biz_b)
				# 检测字符串是否只由数字组成
				if not biz_str.isdigit() or not url.startswith('http://mp.weixin.qq.com/s?__biz='):
					continue
				if line not in quchong:
					quchong.add(line)
					file.writelines(line)
					jishu += 1
					print(jishu)
