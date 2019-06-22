from django.db import models

# Create your models here.

class Site2pars ( models.Model ):
	url = models.URLField ()
	time = models.DateTimeField  ( 'Date to publish' )
	def __str__ ( self ):
		return self.url
