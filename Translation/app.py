# runs the translation  
import tensorflow as tf
from data_helpers import *
from model import Seq2SeqModel
import sys
import numpy as np
import matplotlib.pyplot as plt

from flask import Flask, request, jsonify, abort, send_from_directory

app = Flask(__name__)


rnn_size = 1024
num_layers = 1
embedding_size = 256
learning_rate = 0.001
model_dir = './model4/'
graph_dir = ".graph/"
model_name = 'translation.ckpt'
data = Data()
eng2int = data.eng2int
int2eng = data.int2eng
spa2int = data.spa2int
int2spa = data.int2spa

wordToTranslate = ""

model = Seq2SeqModel(rnn_size, num_layers, embedding_size, eng2int, spa2int, learning_rate, use_attention = True, max_gradient_norm=5.0)
ckpt = tf.train.get_checkpoint_state(model_dir)

if ckpt and tf.train.checkpoint_exists(ckpt.model_checkpoint_path):
        print('Reloading model parameters..')
        model.saver.restore(sess, ckpt.model_checkpoint_path)
else:
    raise ValueError('No such file:[{}]'.format(model_dir))

@app.route('/')
def hello():
    return "Hello"

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    
    wordToTranslate = ""
    
    if(request.method == 'POST'):
        # there should be a catch if the image isnt there
        
        try:
            wordToTranslate = request.json['translate']
        except(TypeError):
            wordToTranslate = request.form['translate']
        
    
    
with tf.compat.v1.Session() as sess:

    batch2, input_tags2= sentence2batch(wordToTranslate, spa2int)
    predicted_ids2, alignments2= model.translation(sess, batch2)
    print("\n The translation of the seoncd sentence is:\n")
    output_tags2 = ids_to_words(predicted_ids2, int2eng)
    
    return ids_to_words
    


if __name__ == '__main__':
 app.run(debug=True)
