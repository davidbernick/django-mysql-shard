import sys,random

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
from django.db import connections, transaction
from django.db.models import loading, Manager, Model, signals
from django.db.models.base import ModelBase, subclass_exception
from django.db.models.fields import PositiveIntegerField
from django.db.models.fields.related import ForeignKey, ManyToOneRel, \
  RECURSIVE_RELATIONSHIP_CONSTANT, ReverseSingleRelatedObjectDescriptor
from django.db.utils import DatabaseError
import bitstring

class ShardDescriptor(ModelBase):
	pass

	
			
class ShardModel(Model):
	__metaclass__ = ShardDescriptor

	class Meta:
		abstract = True

	def get_db_for_write_from_key(self,binarray):
		a = bitstring.BitArray(bin(binarray))
		shard_id = a[41:49].int
		return "shard_host_"+str(shard_id)
	
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
	

	def save(self, *args, **kwargs):
		if self.pk !=0:
			print "update"
			###UPDATE INFO GOES HERE!!!
			db_for_write = self.get_db_for_write_from_key(self.pk)
			super(ShardModel, self).save(using=db_for_write,*args, **kwargs)
		else:
			print "save"
			for f in self._meta.fields:
				if f.name=="id":
					self.pk = f.get_next_value()
			#self.id = self.id.get_next_value()
			db_for_write = self.get_db_for_write_from_key(self.pk)
			super(ShardModel, self).save(using=db_for_write,*args, **kwargs)
			
