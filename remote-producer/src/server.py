import os
from flask import Flask, render_template, flash, request
from flask_restful import Resource, Api, reqparse
from wtforms import Form, validators, StringField, SubmitField, SelectField
import json, sys, re
import publisher
import time

DEBUG = True
PORT = 5000

app = Flask(__name__)
api = Api(app)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
producer = None



class RestKafkaManager(Resource):
    def get(self):
        return kafka_info, 200

    def put(self):
        #print("request.data: {}".format(reqparse.request.data.decode("utf-8") ))
        jm = json.loads(reqparse.request.data.decode("utf-8"))
        kafka_info['topic'] = jm["topic"]
        msg = "New default topic set to " + kafka_info['topic']
        return msg , 200

    def post(self):
        self.put()


class RestKafkaManagerPublish(Resource):
    def put(self):
        jm = json.loads(reqparse.request.data.decode("utf-8"))
        topic = jm.get('topic', kafka_info['topic'])
        batch_size = jm.get('batch_size', kafka_info['batch_size'])
        interval = jm.get('interval', kafka_info['interval'])
        print("Using topic={}, batch_size={}, interval={}".format(topic, batch_size, interval))
        for i in range(0, int(batch_size)):
            w_data = publisher.get_weather_data(publisher.OPEN_WEATHER_LOC, publisher.APP_ID, "metric")
            print("Returned data: {}".format(w_data))
            publisher.publish_data(producer, topic, w_data)
            time.sleep(int(interval))
        return "Done!", 200

    def post(self):
        self.put()
        return "Done!", 200


class ReusableForm(Form):
    topic = StringField('Publish on:', validators=[validators.required()])
    dropdown_list_bs = ['1', '2', '3', '5', '8', '13']
    batch_size = SelectField('Batch size', choices=dropdown_list_bs)
    dropdown_list_ti = ['1', '2', '3', '4', '5']
    time_int = SelectField('Time interval', choices=dropdown_list_ti)



@app.route("/", methods=['GET', 'POST'])
def result():
    form = ReusableForm(request.form)
    print(form.errors)

    if request.method == 'POST':
        topic = request.form['topic']
        batch_size = request.form['batch_size']
        time_int = request.form['time_int']
        #poll_int = 2

        print("topic={}, num messages={}".format(topic, batch_size))

        if form.validate():
            try:
                title = "Kafka Topic: {}, Batch size={}, Time interval={}".format(topic, batch_size, time_int)
                flash(title, 'title')

                for i in range(0, int(batch_size)):
                    w_data = publisher.get_weather_data(publisher.OPEN_WEATHER_LOC, publisher.APP_ID, "metric")
                    print("Returned data: {}".format(w_data))
                    flash('Data', 'key')
                    flash(w_data, 'value')
                    publisher.publish_data(producer, topic, w_data)
                    time.sleep(int(time_int))

            except Exception as e:
                flash(e, 'error')
                print("error"+ e)
        else:
            flash('Form field required.')

    return render_template('result.htm', form=form)


api.add_resource(RestKafkaManager, '/api')
api.add_resource(RestKafkaManagerPublish, '/api/publish')


try:
    kafka_info = {
        'broker': os.environ['KAFKA_BROKER'],
        'topic': publisher.KAFKA_TOPIC,
        'batch_size': 5,
        'interval': 2
    }
except KeyError:
    kafka_info = {
        'broker': 'localhost:19092',
        'topic': publisher.KAFKA_TOPIC,
        'batch_size': 5,
        'interval': 2
    }
    


bs = kafka_info['broker']
producer = publisher.KafkaProducer(bootstrap_servers=bs)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)

