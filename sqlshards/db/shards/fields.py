import random
from django.conf import settings
from django.db import connections, transaction
from django.db.models.fields import AutoField, BigIntegerField
from django.db.models.signals import post_syncdb, class_prepared
from django.db.utils import DatabaseError
from django.utils.translation import ugettext_lazy as _

class AutoSequenceField(BigIntegerField):
	def __init__(self,  *args, **kwargs):
		kwargs['blank'] = True
		kwargs['editable'] = False
		kwargs['unique'] = True
		kwargs['default'] = 0
		super(AutoSequenceField, self).__init__(*args, **kwargs)
		
#	def pre_save(self, model_instance, add):
#		value = getattr(model_instance, self.attname, None)
#		if add and not value:
#			value = self.get_next_value()
#			setattr(model_instance, self.attname, value)
#		return value

	def get_db_for_write(self):
		"""
		Writes anywhere
		"""
		db_name_list=[]
		dbhash = settings.DATABASES
		for key, value in dbhash.iteritems():
			if key.startswith("shard_host_"):
				db_name_list.append(key)
		
		return random.choice(db_name_list)	
	
	def get_next_value(self):
		db_alias = self.get_db_for_write()
		cursor = None
		try:
			cursor = connections[db_alias].cursor()
			#cursor.execute("SELECT NEXTVAL(%s)", (self._sequence,))
			cursor.execute("SELECT next_sharded_id()")
			return cursor.fetchone()[0]
		except Exception,exc:
			print exc
		finally:
			if cursor:
				cursor.close()
