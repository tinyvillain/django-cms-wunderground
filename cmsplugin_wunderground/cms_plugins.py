import urllib2
import json
import datetime

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.cache import cache

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from cmsplugin_wunderground.models import CityWeatherPlugin as CityWeatherPluginModel

class CurrentWeatherPlugin(CMSPluginBase):
	name = _("Current Local Weather")
	render_template = "cmsplugin_wunderground/local_weather.html"
    
	def render(self, context, instance, placeholder):
		request = context['request']
		user_ip_address = request.META['REMOTE_ADDR']
		if user_ip_address == '127.0.0.1':
			user_ip_address = '68.70.92.82'
		cache_key = 'wunderground_result_%s' % user_ip_address
        
		# check for api key
		try:
			wunderground_key = getattr(settings, 'WUNDERGROUND_KEY')
		except AttributeError, NameError:
			raise Exception('WUNDERGROUND_KEY not set in settings')

		weather_url = 'http://api.wunderground.com/api/%s/geolookup/conditions/q/autoip.json?geo_ip=%s' % (wunderground_key, user_ip_address)
		weather_info = cache.get(cache_key)
		if not weather_info:
			wunderground_response = urllib2.urlopen(weather_url)
			weather_info_json = wunderground_response.read()
			weather_info = json.loads(weather_info_json)
			cache.set(cache_key, weather_info, getattr(settings, 'WUNDERGROUND_CACHE_DURATION', 60*60))
            
		context.update({
			'instance': instance,
			'ip': user_ip_address,
			'weather_info': weather_info,
		})
		return context

plugin_pool.register_plugin(CurrentWeatherPlugin)

class CityWeatherPlugin(CMSPluginBase):
	model = CityWeatherPluginModel
	name = _("City Weather Plugin")
	render_template = "cmsplugin_wunderground/city_weather.html"

	def render(self, context, instance, placeholder):
		cache_key_conditions = 'wunderground_result_conditions_city_%s' % instance.city
		cache_key_forecast = 'wunderground_result_forecast_city_%s' % instance.city

		# check for api key
		try:
			wunderground_key = getattr(settings, 'WUNDERGROUND_KEY')
		except AttributeError, NameError:
			raise Exception('WUNDERGROUND_KEY not set in settings')
		
		weather_url = 'http://api.wunderground.com/api/%s/conditions/q/%s.json' % (wunderground_key, instance.city)

		forecast_url = 'http://api.wunderground.com/api/%s/forecast/q/%s.json' % (wunderground_key, instance.city)


		weather_info = cache.get(cache_key_conditions)
		if not weather_info:
			wunderground_response = urllib2.urlopen(weather_url)
			weather_info_json = wunderground_response.read()
			weather_info = json.loads(weather_info_json)
			cache.set(cache_key_conditions, weather_info, getattr(settings, 'WUNDERGROUND_CACHE_DURATION', 60*60))

		forecast_info = cache.get(cache_key_forecast)
		if not forecast_info:
			wunderground_response = urllib2.urlopen(forecast_url)
			forecast_info_json = wunderground_response.read()
			forecast_info = json.loads(forecast_info_json)
			cache.set(cache_key_forecast, forecast_info, getattr(settings, 'WUNDERGROUND_CACHE_DURATION', 60*60))
		
		context.update({
			'instance': instance,
			'weather_info': weather_info,
			'forecast_info': forecast_info,
			'today': datetime.datetime.today()
		})
		return context

plugin_pool.register_plugin(CityWeatherPlugin)
