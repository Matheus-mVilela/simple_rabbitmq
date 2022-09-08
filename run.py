import pika



class BuildRabbitMQ():
    def __init__(self):
        self.connetion = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        self.channel = self.connetion.channel()

        self.exchange_name = 'the_exchange'
        self.first_queue_name = 'the_first_queue'
        self.last_queue_name = 'the_last_queue'
        self.permitted = 'permitted'
        self.no_permitted = 'no_permitted'
    
    def build(self):
        self.channel.exchange_declare(exchange = self.exchange_name, exchange_type = 'direct')
        self.channel.queue_declare(queue = self.first_queue_name, exclusive = True)
        self.channel.queue_declare(queue = self.last_queue_name, exclusive = True)
        self.channel.queue_bind(exchange = self.exchange_name, queue = self.first_queue_name, routing_key = self.permitted)
        self.channel.queue_bind(exchange = self.exchange_name, queue = self.last_queue_name, routing_key = self.no_permitted)
        self.channel.basic_consume(queue = self.first_queue_name, on_message_callback = self.callback, auto_ack = True)
        self.channel.basic_consume(queue = self.last_queue_name, on_message_callback = self.callback, auto_ack = True)

    def callback(self,ch, method, properties, body):
        print(body)

    def subscribe(self):
        self.channel.start_consuming()

    def publish(self):
        first_routing_key = self.permitted
        last_routing_key = self.no_permitted
        message = 'This is test of message!'
        self.channel.basic_publish(exchange=self.exchange_name, routing_key=first_routing_key, body=message)
        self.channel.basic_publish(exchange=self.exchange_name, routing_key=last_routing_key, body=message)
        

