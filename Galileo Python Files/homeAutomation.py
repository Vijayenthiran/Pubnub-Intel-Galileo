#reference used: https://github.com/shyampurk/PubNub-RaspberryPi-RemoteControl
#the code is based on pidriver.py file
#pubnub developer console: http://www.pubnub.com/console/?channel=pubnub-intel-gal-demo&origin=pubsub.pubnub.com&sub=demo&pub=demo&cipher=&ssl=false&secret=&auth=


from pubnub import Pubnub

#GPIO Control
import time
import pyupm_grove as grove

# Create the Grove LED object using GPIO pin 2
led = grove.GroveLed(2)

currentState = 0
respstring = ''

# Print the name
print led.name()

pubnub = Pubnub(publish_key='pub-c-0d652f8b-a119-48b8-b625-9953fdaf67bb', subscribe_key='sub-c-5b803346-6f22-11e5-b932-02ee2ddab7fe')
pubnubChannelName = 'gpio-galileo-control'

#Subscribe (listen on) a channel (it's async!):
def _callback(message, channel):
	#print(message)
	print "message received"
	print message
	global respstring, currentState
	if message == {u'req': u'toggle'}:
		if currentState == 0:
			currentState =1
			led.on()
			respstring = 'on'
		else:
			currentState =0
			led.off()
			respstring = 'off'

	#sending back a response
	respmsg = {"resp" : respstring }
	pubnub.publish(pubnubChannelName, respmsg)
	 
def _error(message):
    #print(message)
    print "error"

pubnub.subscribe(channels=pubnubChannelName, callback=_callback, error=_error)