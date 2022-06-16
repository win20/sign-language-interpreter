import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

import pandas as pd
import numpy as np


def main():
    # load and split data
    data = pd.read_csv('data_to_be_read.csv')
    dataset = data.values
    X = dataset[:, 0:140].astype(float)

    # load and process model
    model = tf.keras.models.load_model('../model_training/saved_models/no_scaling/')
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

    # make predictions on data and find most common prediction
    predictions = probability_model.predict(X)
    prediction_indices = []
    for item in predictions:
        prediction_indices.append(np.argmax(item))

    # get the most common prediction
    counter = 0
    max_num = prediction_indices[0]
    for item in prediction_indices:
        current_frequency = prediction_indices.count(item)
        if current_frequency > counter:
            counter = current_frequency
            max_num = item

    # get label
    labels = ['eight', 'five', 'four', 'nine', 'one', 'seven', 'six', 'ten', 'three', 'two', 'zero']
    print(labels[max_num] + '\n')


if __name__ == '__main__':
    main()

