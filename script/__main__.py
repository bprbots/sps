from hashlib import sha256
from requests import get,post

password = sha256("^Ba12011385$".encode()).hexdigest()
result = post(
	data={
		"password":password
	},
	url="http://127.0.0.1:5000/todos"
)

print(result.text)