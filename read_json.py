import json
import re

# with open('users.json', 'r') as read_users:
#     read_data = json.load(read_users)
#     read_users.close()
result = '{[123]}'
print(result)
# result = json.dumps(read_data)
result = re.sub(r']}$', '', result)
print(result)

