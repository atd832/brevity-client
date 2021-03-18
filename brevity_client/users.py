
class User:
	def __init__(self, name=''):
		self.name = name
		self.status = ''


class UserGroup:
	def __init__(self, name=''):
		self.name = name
		self.users = {}

	def add_user(self, user: User):
		self.users[user] = 1

	def remove_user(self, user):
		self.users.pop(user)

	def __iter__(self):
		for user in self.users.keys():
			yield user

