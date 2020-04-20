# Heverywhere
Código para obtener los datos de un modulo GPS usando una raspberry.
El codigo hace uso de dos librerias necesarias de instalar (pynmea2 y pika)
pynmea2 para obtener los datos del gps 
Pika es necesaria para establece conexion con el servidor en la nube (Rabbit MQ), en el cual se estarán mandando los 
datos cada 30 minutos.

