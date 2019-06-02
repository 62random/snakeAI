from game import *
from game_runner import *
from learning_model import *
from learning_memory import *
import tensorflow as tf
from matplotlib import pyplot as plt
import curses

BATCH_SIZE = 20
MAX_EPSILON = 0.95
MIN_EPSILON = 0.05
LAMBDA = 0.05


env = Game()
num_states = 12
num_actions = 4





model = Model(num_states, num_actions, BATCH_SIZE)
mem = Memory(50000)

with tf.Session() as sess:
    sess.run(model._var_init)
    gr = GameRunner(sess, model, env, mem, MAX_EPSILON, MIN_EPSILON,
                    LAMBDA)
    num_episodes = 5000
    cnt = 0
    while cnt < num_episodes:
        #if cnt % 100 == 0:
            #gr._rendering = True
            #env._render(True)
            #print('Episode {} of {}'.format(cnt+1, num_episodes))
        gr.run()
        #if cnt % 100 == 0:
            #gr._rendering = False
        cnt += 1
    plt.plot(gr._reward_store)
    plt.show()
    plt.close("all")
    plt.plot(gr._max_x_store)
    plt.show()
