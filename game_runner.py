import random
import numpy as np
import math
import time

GAMMA = 1

class GameRunner:
    def __init__(self, sess, model, env, memory, max_eps, min_eps, decay, render=True):
        self._sess = sess
        self._env = env
        self._model = model
        self._memory = memory
        self._render = render
        self._max_eps = max_eps
        self._min_eps = min_eps
        self._decay = decay
        self._eps = self._max_eps
        self._steps = 0
        self._reward_store = []
        self._max_s_store = []
        self._rendering = False

    def run(self):
        state = self._env._reset()
        self.tot_reward = 0
        max_s = 3
        while True:
            if self._rendering:
                time.sleep(0.025)
            action = self._choose_action(state)
            next_state, reward, done, size = self._env._step(action)
            if size > max_s:
                max_s = size

            if done:
                next_state = None

            self._memory.add_sample((state, action, reward, next_state))
            self._replay()

            self._steps += 1
            self._eps = self._min_eps + (self._max_eps - self._min_eps)* math.exp(-self._decay * self._steps)

            state = next_state
            self.tot_reward += reward

            if done:
                self._reward_store.append(self.tot_reward)
                self._max_s_store.append(max_s)
                break

    def _choose_action(self, state):
        if random.random() < self._eps:
            return random.randint(0, self._model._num_actions - 1)
        else:
            return np.argmax(self._model.predict_one(state, self._sess))

    def _replay(self):
        batch = self._memory.sample(self._model._batch_size)
        states = np.array([val[0] for val in batch])
        next_states = np.array([(np.zeros(self._model._num_states) if val[3] is None else val[3]) for val in batch])

        q_s_a = self._model.predict_batch(states, self._sess)
        q_s_a_d = self._model.predict_batch(next_states, self._sess)

        x = np.zeros((len(batch), self._model._num_states))
        y = np.zeros((len(batch), self._model._num_actions))

        for i,b in enumerate(batch):
            state, action, reward, next_state = b[0], b[1], b[2], b[3]
            current_q = q_s_a[i]
            if next_state is None:
                current_q[action] = reward
            else:
                current_q[action] = reward + GAMMA * np.amax(q_s_a_d[i])
            x[i] = state
            y[i] = current_q

        self._model.train_batch(self._sess, x, y)
