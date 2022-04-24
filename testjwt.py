import jwt 
from datetime import datetime

test_jwt = jwt.encode({'pretty':'printed'},'donttellanyone')

print(test_jwt)

test_jwt1 = jwt.decode(test_jwt,'donttellanyone',algorithms='HS256')
print(test_jwt1)


salt = '123456'
headers = {
    'type':'jwt',
    'alg':'HS256'
}
create_time =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
payload ={
    'user_id':'123',
    'user_email':'123',
    'user_password':'123' ,
    'usre_cread_time': create_time
}
test_jwt2 = jwt.encode(payload,salt,algorithm='HS2565',headers=headers)

print(test_jwt2)

test_jwt3 = jwt.decode(test_jwt2,salt,algorithms='HS256')
print(test_jwt3)
