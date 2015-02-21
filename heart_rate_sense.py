import time, yaml, sys, os, signal, httplib, urllib
import RPi.GPIO as GPIO                                                                                                                           


dir="/root/"
timestamp=time.strftime("D%Y%m%d_T%H%M%S")
conf=dir + "heartbeat_"+timestamp+".yml"

#free green led from MMC
os.system("echo none >/sys/class/leds/led0/trigger")
                                                                                  
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN)
l=[]


def signal_handler(signal, frame):

	print "Interrupted/terminated"
	print "Gracefully exiting..."
	os.system("echo mmc0 >/sys/class/leds/led0/trigger")



	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)






def load_stats_file(self):
	#load 
	f = open(conf, "r")
	conf_yaml=f.read()
	progs = yaml.load(conf_yaml)
	f.close()
	return progs


def save_file(file):

	f = open(conf, "w")
	conf_yaml=yaml.dump(file)
	f.write(conf_yaml)
	f.close()


def post_thingspeak(rate):


#keep the names field1 and field2 etc... they are hardcoded                                                                                                                                                    

	params1 = urllib.urlencode({'field1': rate, 'key':'S4ECP6KFLA3U0Y4A'})
                                                                                                               
	headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPConnection("api.thingspeak.com:80")
	try:
		conn.request("POST", "/update", params1, headers)
		response = conn.getresponse()
		print response.status, response.reason
		data = response.read()
                conn.close()


	except:
		print  "connection failed!"







def NoteBeat(channel):

	l.append(time.time())
	sys.stdout.write('O')
	sys.stdout.flush()
	os.system("echo 1 >/sys/class/leds/led0/brightness")
	os.system("echo 0 >/sys/class/leds/led0/brightness")


GPIO.add_event_detect(25, GPIO.RISING, callback=NoteBeat, bouncetime=300)
samples=30
while True == True:
	time.sleep(30)
	end=len(l)-1
	last30 = []
	if end >= 30:
		for element in range(end-samples,end):
			last30.append(l[element])
	
	
	       	first=last30[0]
		last=last30[len(last30)-1]
	
		time_passed=last-first
		beats = len(last30)
	
		heart_rate = int(60*beats/time_passed)
		print "stats:" 
		print "beats so far: ", len(l), " current average last30: ", str(heart_rate)
	
		save_file(l)
		post_thingspeak(heart_rate)
 



