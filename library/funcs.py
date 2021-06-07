import json


def open_user(user):
	users = get_users_data()
	if str(user.id) in users:
		return False
	else:
		users[str(user.id)] = {}
		users[str(user.id)]["mmts"] = 0

	with open('data/bank.json','w') as f:
		json.dump(users,f)

	return True
def get_users_data():
	with open('data/bank.json','r') as f:
		users = json.load(f)

	return users

def dump(users):
	with open('data/bank.json','w') as f:
		json.dump(users,f)

def addmod(user, category:str="general",type="mods"):
	with open('data/allocs.json','r') as f:
		main = json.load(f)
	if type == 'mods' or type == 'tmods':
		maxlen = 10
	elif type == "smods":
		maxlen = 2
	length = len(main["main"][category][type])
	if length >= maxlen:
		return 1
	try:
		alrcateg = main["users"][str(user.id)]
	except KeyError:
		alrcateg = None
	if alrcateg != None:
		main["main"][alrcateg][type].remove(user.id)
	if user.id in main["main"][category][type] or category == alrcateg:
		return 2
	main["main"][category][type].append(user.id)
	main["users"][str(user.id)] = category
	with open('data/allocs.json','w') as f:
		json.dump(main,f)