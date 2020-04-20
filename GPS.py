import serial
import time
import string
import pynmea2 #libreria para poder obtener datos del modulo gps
import pika #libreria para poder envíar los datos atraves de Rabbit MQ

connection = pika.BlockingConnection(pika.ConnectionParameters('amqp://192.168.43.232')) #!Linea para acceder a la cuenta de Rabbit y hacer uso de ella
channel = connection.channel() #Conexion a RabbitMQ

while True:
    port="/dev/ttyAMA0" #puerto que se habilito para el modulo GPS de acuerdo a la raspberry
    ser=serial.Serial(port, baudrate=9600, timeout=.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata=ser.readline() #En este linea se reciben los datos que manda el GPS

    if newdata[0:6] == "GPGPLL": #Aqui se pregunta si el dato que se esta recibiendo es de tipo GPGLL (Geographic Position Latitude/Longitude)
        newmsg=pynmea2.parse(newdata) #Si la condicion es correcta se acepta el GPLL (esto porque el gps no manda siempre las coordenadas correctas)
        lat=newmsg.latitude #Se renombra para darle nombre a las coordenadas latitud /longitud
        lng=newmsg.longitude #Longitud
        channel.queue_declare(queue='GPS') #Rabbit MQ trabaja con colas y aqui se le asigana el nombre de nuestra cola que en este caso la nombramos GPS
        gps = "Latitude= " + str(lat) + " and longitude= "+ str(lng)
        channel.basic_publish(exchange='', #Mandamos las variables latitud y longitud
                      routing_key='Latitude',
                      body='Longitude')
        print(gps) #mandamos e imprimimos nuestras coordenadas
        time.sleep(1800) #Tiempo de espera para que se mande cada media hora como se establecio en el proyecto
