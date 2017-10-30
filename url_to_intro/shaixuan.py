import codecs
import base64
from traceback import print_exc

# file_list = ['gzhUrl_bj_1015_1.log', 'gzhUrl_bj_1015_2.log', 'gzhUrl_bj_1015_3.log', 'gzhUrl_bj_1015_4.log',
#              'gzhUrl_sh_1015_1.log', 'gzhUrl_sh_1015_2.log', 'gzhUrl_sh_1015_3.log']
file_list = ['/Users/menggui/Desktop/project/weixin/url_to_intro/gzhUrl_zhejiang_1022_quchong.log']
# path_list = ['public_num.log']
# cp1252
jishu = 0
quchong = set()
for name in file_list:
	with codecs.open('weixin_quchong_all_1.log', 'a', 'cp1252') as file:
		with codecs.open(name, 'r', 'cp1252') as f:
			# print(f.read(36027951))
			for line in f.readlines():
				try:
					# biz_b = line[:16]
					# url = line[17:]
					x = line.split('	') if '	' in line else line.split('	')
					if len(x) < 2:
						continue
					biz_b = x[0].replace('??', '')
					url = x[1]
					# biz_str = base64.urlsafe_b64decode(biz_b)
					# 检测字符串是否只由数字组成
					# if not biz_str.isdigit() or not url.startswith('http://mp.weixin.qq.com/s?__biz='):
					# 	continue
					if not url.startswith('http://mp.weixin.qq.com/s?__biz='):
						continue
					line = biz_b + '	' + url
					if line not in quchong:
						quchong.add(line)
						file.writelines(line)
						jishu += 1
						print(jishu)
				except:
					print_exc()
					continue
