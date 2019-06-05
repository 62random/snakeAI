from __future__ import division
from game import *
from game_runner import *
from learning_model import *
from learning_memory import *
import tensorflow as tf
from matplotlib import pyplot as plt
import curses

BATCH_SIZE = 20
MAX_EPSILON = 0.9
MIN_EPSILON = 0.00001
LAMBDA = 0.005


env = Game()
num_states = 14
num_actions = 4





model = Model(num_states, num_actions, BATCH_SIZE)
mem = Memory(50000000)

with tf.Session() as sess:
    sess.run(model._var_init)
    gr = GameRunner(sess, model, env, mem, MAX_EPSILON, MIN_EPSILON,
                    LAMBDA)
    num_episodes = 10000
    cnt = 0
    while cnt < num_episodes:
        if cnt == num_episodes - 10:
            gr._rendering = True
            env._render(True)
            #print('Episode {} of {}'.format(cnt+1, num_episodes))
        gr.run()
        print("Episode {},\t Total reward: {},\t Size: {},\t Steps: {},\t Eps: {}".format(cnt, gr.tot_reward, len(gr._env.snake.parts), gr._env.steps, gr._eps))
        #if cnt % 100 == 0:
            #gr._rendering = False
        cnt += 1

    avg = [3]
    for i in range(1,len(gr._max_s_store)):
        avg.append(sum(gr._max_s_store[:i])/len(gr._max_s_store[:i]))

    plt.plot(gr._reward_store)
    plt.show()
    plt.close("all")
    plt.plot(gr._max_s_store)
    plt.plot(avg)
    plt.show()
