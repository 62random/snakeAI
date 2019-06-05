import tensorflow as tf
import numpy as np
import os

#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#tf.logging.set_verbosity(tf.logging.ERROR)

class Model:
    def __init__(self, num_states, num_actions, batch_size):
        self._num_states = num_states
        self._num_actions = num_actions
        self._batch_size = batch_size
        #placeholders
        self._states = None
        self._actions = None
        #output
        self._logits = None
        self._optimizer = None
        self._var_init = None
        #model setup
        self._define_model()

    def _define_model(self):
        self._states = tf.placeholder(shape = [None, self._num_states], dtype=tf.float32)
        self._q_s_a = tf.placeholder(shape = [None, self._num_actions], dtype=tf.float32)
        #fully connected hidden layers
        fc1 = tf.layers.dense(self._states, 36, activation=tf.nn.relu)
        fc2 = tf.layers.dense(fc1, 36, activation=tf.nn.relu)
        self._logits = tf.layers.dense(fc2, self._num_actions)
        loss = tf.losses.mean_squared_error(self._q_s_a, self._logits)
        self._optimizer = tf.train.AdamOptimizer().minimize(loss)
        self._var_init = tf.global_variables_initializer()

    def predict_one(self, state, sess):
        return sess.run(self._logits, feed_dict= {self._states:
                                                        np.array(state).reshape(1, self._num_states)})

    def predict_batch(self, states, sess):
        return sess.run(self._logits, feed_dict={self._states: states})

    def train_batch(self, sess, x_batch, y_batch):
        sess.run(self._optimizer, feed_dict={self._states: x_batch, self._q_s_a: y_batch})
