from twilio.rest import Client
from credentials import *
from datetime import datetime
import urllib.request, json
import smtplib

client = Client(account_sid, auth_token)

class User:
	def __init__(self, name, number, zipcode, carrier):
		self.name = name
		self.number = number
		self.zipcode = zipcode
		self.carrier = carrier

users = []
# users.append(User('Sam Tubb', '8646067250', '29316', 'MetroPCS'))
users.append(User('Richard Red', '6787733594', '30601', 'TMobile'))
# users.append(User('Kenny Kim', '8474140183', '30118', 'Sprint'))
# users.append(User('Jay Tang', '6789869272', '30601', 'Verizon'))
# users.append(User('Caitlin Eng', '5163025963', '14850', 'Verizon'))
# users.append(User('Kok Seng Tan', '6788637883', '30363', 'Verizon'))
# users.append(User('Jinyong Jeong', '7066167044', '30601', 'Verizon'))
users.append(User('Thomas Yoo', '4045141015', '30601', 'AT&T'))
# users.append(User('Brandon Cho', '6782676899', '60201', 'AT&T'))

def create_message(zipcode):
	api_url = 'http://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',us&appid='+weather_apikey
	with urllib.request.urlopen(api_url) as url:
		data = json.loads(url.read().decode())

	temp_k = data['main']['temp']
	temp_c = temp_k - 273.15
	temp_f = (temp_c * 1.8) + 32

	text = 'The current temperature is {:.2f}'.format(temp_f)+'F ({:.2f}'.format(temp_c)+'C). '
	if temp_f >= 65:
		text += 'You don\'t need a jacket today.'
	elif 45 <= temp_f < 65:
		text += 'You should wear a jacket today.'
	elif temp_f < 45:
		text += 'It\'s very cold today, you probably need more than a jacket.'
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
	notify()
	print('=====================================================================================')

if __name__ == '__main__':
	main()