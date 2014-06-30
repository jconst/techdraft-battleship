import requests
from random import randint

def flatten(list_to_flatten):
    for elem in list_to_flatten:
        if isinstance(elem,(list, tuple)):
            for x in flatten(elem):
                yield x
        else:
            yield elem

def pos_to_char(pos):
    return chr(pos + ord('A'))

def populateBoard():
	return [[pos_to_char(c)+str(r) for r in range(1,11)] for c in range(10)]

def available(shots):
	return [s for s in shots if s not in ["HIT", "MISS"]]

def makeShot(loc, url):
	print "shooting %s" % loc		
	
	endpt = "%s/%s" % (url, loc)
	resp = requests.post(endpt)
	print resp.json()
	return resp.json()

req = requests.get("https://student.people.co/api/challenge/battleship/09120dc84c69/boards")

boards = [b for b in req.json() if b["is_test"]]

for board in boards:
	shots = populateBoard()
	print shots
	while not board["is_finished"]:
		
		flat = available(flatten(shots))
		ind = randint(len(shots))
		loc = flat[ind]
		resp = makeShot(loc, board["url"])
		shots[col][row] = "HIT" if resp["is_hit"] else "MISS"
		
		newReq = requests.get(board["url"])
		board = dict(board.items() + newReq.json().items()) 
	