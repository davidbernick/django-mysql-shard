import random
from django.conf import settings

class RandomWriteRouter(object):

	def db_for_write(self, model, **hints):
		"""
		Writes anywhere
		"""
		db_name_list=[]
		dbhash = settings.DATABASES
		for key, value in dbhash.iteritems():
			if key.startswith("shard_host_"):
				db_name_list.append(key)
		
		return random.choice(db_name_list)