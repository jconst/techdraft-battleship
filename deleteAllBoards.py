import requests

req = requests.get("https://student.people.co/api/challenge/battleship/09120dc84c69/boards")

boards = [b for b in req.json() if b["is_test"]]

for board in boards:
	print requests.delete(board["url"]).status_code
	
