import requests
from random import randrange

def flatten(list_to_flatten):
    for elem in list_to_flatten:
        if isinstance(elem,(list, tuple)):
            for x in flatten(elem):
                yield x
        else:
            yield elem

def pos_to_char(pos):
    return chr(pos + ord('A'))

def char_position(letter):
    return ord(letter) - ord('A')

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
	hor = 0
	vert = 0
	firstHit = None

	while not board["is_finished"]:
		
		
		flat = available(flatten(shots))
		ind = randrange(len(flat))
		loc, col, row = None, 0, 0
		
		if firstHit:
#			while loc in ["MISS", "HIT", ""]:
			if not (firstHit[0]+hor < 10 and firstHit[1]+vert < 10 and 
					firstHit[0]+hor >= 0 and firstHit[1]+vert >= 0):
				loc = None
				break
			loc = shots[firstHit[0]+hor][firstHit[1]+vert]
			if loc in ["MISS", "HIT"]:
				loc = None
		
		if not loc:
			loc = flat[ind]
			col = char_position(loc[0])
			row = int(loc[1]) - 1
			
		resp = makeShot(loc, board["url"])
		if resp["is_hit"]:
			shots[col][row] = "HIT"
			if hor == 0 and vert == 0:
				firstHit = (col, row)
				hor = 1
			elif hor > 0:
				hor += 1
			elif hor < 0:
				hor -= 1
			elif vert > 0:
				vert += 1
			elif vert < 0:
				vert -= 1
				
		else:
			shots[col][row] = "MISS"
			if hor == 0 and vert == 0:
				hor = 1
			if hor > 0:
				hor == -1
			elif hor < 0:
				hor = 0
				vert = 1
			elif vert > 0:
				vert == -1
			elif vert < 0:
				hor = 0
				vert = 0
				firstHit = None
		
		if resp["sunk"]:
			hor = 0
			vert = 0
			firstHit = None
		
		newReq = requests.get(board["url"])
		board = dict(board.items() + newReq.json().items()) 
	