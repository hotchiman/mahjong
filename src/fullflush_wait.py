def check_tehai(haishi):
	# input_tehai = input("入力:")

	# エラー処理
	if (not haishi.isdecimal()):
		message = "手牌を整数値で入力してください。（例：112233444567）"
		isError = True
	elif (len(haishi) % 3 == 1):
		message = "多牌です。手牌は3の倍数で入力してください（例：224567）"
		isError = True
	elif (len(haishi) % 3 == 2):
		message = "少牌です。手牌は3の倍数で入力してください（例：224567）"
		isError = True
	elif (haishi.count("0") >= 1):
		message = "0は入力できません。"
		isError = True
	elif (len(tehai_count(haishi,5)) >= 1):
		message = "同じ牌は5つ以上入力できません。"
		isError = True
	else:
		message = ""
		isError = False
		
	return isError, message
		
def tehai_count(line,max_num):
	cnt = 1
	max = 1
	max_hai = []
	
	line_sort = ''.join(sorted(line))
	for i in range(1,len(line_sort)):
		if line_sort[i] == line_sort[i-1]:
			cnt += 1
			if(cnt >= max_num):
				max_hai.append(line_sort[i-1])
			if cnt > max:
				max = cnt
		else:
			cnt = 1
			
	return list(set(max_hai))
	
def ripai(tehai_str):
	# 手牌のリスト化
	tehai_list = tehai_list_conv(tehai_str)
	# 手牌の文字列化
	ripai = tehai_str_conv(tehai_list)
	return ripai
	
# 手牌のリスト化
def tehai_list_conv(tehai_str):
	tehai_lst = [0] * 10
	for hai in tehai_str:
		tehai_lst[int(hai)] += 1
	return tehai_lst

# 手牌の文字列化
def tehai_str_conv(tehai_lst):
	tehai_str = ""
	for i in range(1,len(tehai_lst)):
		for num in range(tehai_lst[i]):
			tehai_str += str(i)
	return tehai_str

def agari_check(input_num):

	tehai_list_default = [0] * 10
	agari_hai_dict = {}

	# 手牌にマイティ牌を補充
	for hokan_hai in range(1,10):
		# 同一牌5枚目は使用不可
		if(str(hokan_hai) in tehai_count(input_num,4)): continue
		tehai = input_num + str(hokan_hai)
		
		# 牌をつもる
		for tsumo_hai in range(1,10):
			# 同一牌5枚目はツモれない
			if(str(tsumo_hai) in tehai_count(tehai,4)): continue
			tsumo = tehai + str(tsumo_hai)
			
			# 手牌の初期化
			tehai_list = tehai_list_default[:]
			
			# 手牌のリスト化
			tehai_list = tehai_list_conv(tsumo)

			atama = 0
			tehai_list_copy = tehai_list[:]
			
			# マイティ牌を補充した手牌+ツモ牌=和了系かチェック
			for i in range(len(tehai_list)):
				# 手牌の初期化
				tehai_list = tehai_list_copy[:]
				
				# 雀頭を探索して消去する
				if(tehai_list[i] >= 2):
					tehai_list[i] -= 2
					atama = 1;
				
				if(atama == 1):
					for j in range(len(tehai_list)-1):
						# 刻子を探索して削除する
						if(tehai_list[j] == 0 and tehai_list[j+1] >= 3):
							tehai_list[j+1] -= 3
						# 順子を探索して消去する
						if(j < len(tehai_list)-3):
							# 順子ひとつ消去
							if(tehai_list[j] == 0 and tehai_list[j+1] == 1 and tehai_list[j+2] >= 1 and tehai_list[j+3] >= 1):
								tehai_list[j+1] -= 1
								tehai_list[j+2] -= 1
								tehai_list[j+3] -= 1
							# 順子ふたつ消去（二盃口系を削除）
							if(tehai_list[j] == 0 and tehai_list[j+1] == 2 and tehai_list[j+2] >= 2 and tehai_list[j+3] >= 2):
								tehai_list[j+1] -= 2
								tehai_list[j+2] -= 2
								tehai_list[j+3] -= 2
					
				# 和了形のとき、リストの合計値が0になる
				if(sum(tehai_list) == 0): 
					break
				else:
					atama = 0

			if(sum(tehai_list) != 0):
				tehai_list = tehai_list_copy[:]
				chitoi = 0
				for i in range(len(tehai_list)):
					# 七対子系を探索
					if(tehai_list[i] == 2 or tehai_list[i] == 4):
						chitoi += tehai_list[i] / 2
			
			if(sum(tehai_list) == 0 or chitoi == 7):
				# 補完牌と和了牌の紐付け
				if(agari_hai_dict.get(hokan_hai) is None):
					agari_hai_dict[hokan_hai] = str(tsumo_hai)
				else:
					agari_hai_dict[hokan_hai] += str(tsumo_hai)

	agari_str = ""
	for agari_hai in list(agari_hai_dict.values()):
		agari_str += agari_hai
		


	# 理牌
	# print("理牌:" + ripai(input_num))

	if(agari_str == ""):
		# print("ノーテン！")
		agari_str = "ノーテン！"
	# else:
		# print("和了牌:"+ ''.join(sorted(set(agari_str))))
		# print("※")
		# for mykey, myvalue in agari_hai_dict.items():
			# print("補完牌" + str(mykey) + "とすると 和了牌" + myvalue)

	return ''.join(sorted(set(agari_str)))


# 入力
# input_num = tehai_input()

# 和了チェック
# agari_hai = agari_check(input_num)
