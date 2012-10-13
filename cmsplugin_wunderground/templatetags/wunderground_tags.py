from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def wunderground_to_climacons(value, arg='day'):
	# Mapping form
	# http://www.nickschaden.com/weather/js/main.min.js?10015

	day_dict = {
		"chanceflurries":"p",
		"chancerain":"0",
		"chancesleet":"r",
		"chancesnow":"\\",
		"chancetstorms":"x",
		"clear":"v",
		"cloudy":"`",
		"drizzle":"6",
		"flurries":"o",
		"fog":"g",
		"hazy":"v",
		"mostlycloudy":"`",
		"mostlysunny":"v",
		"partlycloudy":"1",
		"partlysunny":"1",
		"rain":"9",
		"sleet":"e",
		"snow":"o",
		"sunny":"v",
		"tstorms":"z",
		"unknown":"s"
	}
	
	night_dict = {
		"chanceflurries":"[",
		"chancerain":"-",
		"chancesleet":"t",
		"chancesnow":"a",
		"chancetstorms":"c",
		"clear":"/",
		"cloudy":"`",
		"drizzle":"6",
		"flurries":"o",
		"fog":"g",
		"hazy":"v",
		"mostlycloudy":"`",
		"mostlysunny":"v",
		"partlycloudy":"2",
		"partlysunny":"2",
		"rain":"9",
		"sleet":"e",
		"snow":"o",
		"sunny":"/",
		"tstorms":"z",
		"unknown":"s"
	}

	if arg == 'day':
		use_dict = day_dict
	else:
		use_dict = night_dict
	
	try:
		return use_dict[value]
	except KeyError:
		return use_dict['unknown']