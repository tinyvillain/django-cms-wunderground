from django.db import models

from cms.models.pluginmodel import CMSPlugin

class CityWeatherPlugin(CMSPlugin):
	city = models.CharField(max_length=50)