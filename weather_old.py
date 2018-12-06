from twilio.rest import Client
from credentials import *
from datetime import datetime
import urllib.request, json
import smtplib

client = Client(account_sid, auth_token)

def owmCall(zipcode):
	api_url = 'http://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',us&appid='+weather_apikey
	with urllib.request.urlopen(api_url) as url:
		data = json.loads(url.read().decode())
	return data


def tempConvert(temp,type):
	#return celc
	if type=='c':
		return temp-273.15
	#return faren
	if type=='f':
		return ((temp-273.15)*1.8)+32

def weather_info(zipcode):

	data=apiCall("current",zipcode)
	data_daily=apiCall("daily",zipcode)

	print (data_daily)

	#print()
	temp = data['main']['temp']
	minTemp = data['main']['temp_min']
	maxTemp = data['main']['temp_max']
	location = data['name']
	return temp,minTemp,maxTemp,location

def create_message(zipcode):
	temp,minTemp,maxTemp,location = weather_info(zipcode)

	text = "\nThe temperature in {} is going to range from {:.2f}F to {:.2f}F ({:.2f}C to {:.2f}C)"
	text=text.format(location,tempConvert(minTemp,'f'),tempConvert(maxTemp,'f'),tempConvert(minTemp,'c'),tempConvert(maxTemp,'c'))
	text += '\nThe current temperature is {:.2f}F ({:.2f}C).'
	text=text.format(tempConvert(temp,'f'),tempConvert(temp,'c'))

	return text

def send_twilio(name, number, message):
	try:
		message = client.messages.create(to='+1'+number, from_=my_twilio, body=message)
		print('Message successfully sent to '+name+' via Twilio SMS.')
	except Exception as e:
		print(e)

def notify():
	s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	s.login('yoyobrains0@gmail.com', mail_pass)
	for x in users:
		print (x.zipcode)
		text = create_message(x.zipcode)
		if x.carrier == 'TMobile' or x.carrier == 'MetroPCS':
			send_twilio(x.name, x.number, text)
		else:
			gateway_address = ''
			if x.carrier == 'Verizon':
				gateway_address = '@vtext.com'
			elif x.carrier == 'Sprint':
				gateway_address = '@messaging.sprintpcs.com'
			elif x.carrier == 'AT&T':
				gateway_address = '@txt.att.net'

			try:
				s.sendmail('Weather', x.number+gateway_address, text)
				print('Message successfully sent to '+x.name+' at '+x.number+' via '+x.carrier+' SMTP-SMS gateway.')
			except Exception as e:
				print(e)
	s.quit()

def main():
	print(datetime.now())
	#notify()
	print(create_message("29316"))
	print('=====================================================================================')

if __name__ == '__main__':
	main()
