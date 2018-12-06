from weather import Weather, Unit
from yweather import Client as YClient
from twilio.rest import Client
from credentials import *
from datetime import datetime
import urllib.request, json
import smtplib

client = Client(account_sid, auth_token)
yweather = YClient()

def weather_info(zip):
    weather = Weather(unit=Unit.FAHRENHEIT)
    woe=yweather.fetch_woeid(zip)
    lookup = weather.lookup(woe)
    condition = lookup.condition
    forecasts = lookup.forecast

    return condition

def create_message(zip):
    info = weather_info(zip);
    print (vars(info));
    text = ""

    text=str(vars(info))
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
			gateway_address = CARRIERS[x.carrier]

			try:
				s.sendmail('Weather', x.number+gateway_address, text)
				print('Message successfully sent to '+x.name+' at '+x.number+' via '+x.carrier+' SMTP-SMS gateway.')
			except Exception as e:
				print(e)
	s.quit()

def main():

    create_message('29316')
    #notify()



if __name__ == '__main__':
	main()
