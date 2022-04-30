import pika
import requests

connection = pika.BlockingConnection(
		pika.ConnectionParameters(host='localhost')
	)

channel = connection.channel()

def callback(ch, method, properties, body):
	print("[x] Received %r" %body)
	x = body.decode("utf-8").split(" ")
	temp_list = [float(i) for i in x]
	avg = sum(temp_list)/len(temp_list)
	avg_temp = str(round(avg, 2))
	print(avg_temp)
	requests.post('http://127.0.0.1:5000/about', data=avg_temp)


channel.basic_consume(
	queue='hello', on_message_callback=callback, auto_ack=True)

print('[*] Waiting for messages to exit press command+c')

channel.start_consuming()





