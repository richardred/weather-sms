from weather import Weather, Unit
from yweather import Client as YClient
from twilio.rest import Client
from credentials import *
from datetime import datetime

client = Client(account_sid, auth_token)
yweather = YClient()

CONDITIONAL_STATEMENTS={
"chilly":"\nIt's a bit chilly. We recommend wearing a sweater or light jacket.",
"coldAF":"\nIt's incredibly cold! We recommend wearing several layers to keep warm!",
"fair":"\nThe temperature is fair. No special clothing recommendations.",
"warm":"\nIt's going to be a bit warm. We advise dressing lighter than normal.",
"hotAF":"\nIt's going to be a hot one! Dress lightly!",
}

def condition_generator(data):
    temp = data['condition'].temp
    if int(temp)<55:
        print(CONDITIONAL_STATEMENTS['coldAF'])
    elif int(temp)<65:
        print(CONDITIONAL_STATEMENTS['chilly'])


def weather_info(zip):
    weather = Weather(unit=Unit.FAHRENHEIT)
    woe=yweather.fetch_woeid(zip)
    lookup = weather.lookup(woe)
    location = lookup.title.strip("Yahoo! Weather - ")
    return {'condition':lookup.condition,'forecasts':lookup.forecast,'astronomy':lookup.astronomy,'location':location}

def create_message(zip):
    info = weather_info(zip);
    text = "It is {}F in {}.".format(info['condition'].temp,info['location'])
    text += "\nThe skies are "+info['condition'].text
    print(text)
    condition_generator(info)
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

    #enter zip code here
    for f in users:
        print("zip: "+f.zipcode+"\n")
        create_message(f.zipcode)
    #notify()



if __name__ == '__main__':
	main()
