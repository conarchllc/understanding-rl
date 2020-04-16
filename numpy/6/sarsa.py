import numpy as np
from td import TD
import time

class Sarsa(TD):
  def __init__(self, env, step_size=0.1, gamma=1, eps=0.1, pol_deriv=None):
    super().__init__(env, None, step_size, gamma) 
    self.eps = eps
    self.pol_deriv = pol_deriv if pol_deriv is not None else self.eps_gre(eps)
    self.reset() 
    print(f"step size: {self.step_size}")
    print(f"epsilon: {self.eps}")
    print(f"gamma: {self.gamma}")

  def best_action(self, moves, vals):
    return moves[np.random.choice(np.flatnonzero(vals == vals.max()))]

  def random_move(self, s):
    return self.env.moves_d[s][np.random.randint(len(self.env.moves_d[s]))]

  def eps_gre(self, eps):
    def eps_gre_pol(s):
      if np.random.random() < self.eps:
        return self.random_move(s)
      return self.best_action(self.env.moves_d[s], np.array([self.Q[(s, a)] for a in self.env.moves_d[s]]))
    return eps_gre_pol 

  def sarsa_update(self, s, a, r, s_p, a_p):
    self.Q[(s, a)] += self.step_size * (r + self.gamma * self.Q[(s_p, a_p)] - self.Q[(s, a)])

  def on_policy_td_control(self, n_episodes):
    ep_per_timesteps = []
    for ep_nb in range(n_episodes):
      ep_start = time.time()
      s = self.env.reset()
      a = self.pol_deriv(s)
      while True:
        #if ep_nb == n_episodes - 1:
        #  print(self.env)
        #  input()
        ep_per_timesteps.append(ep_nb)
        s_p, r, d, _ = self.env.step(a) 
        a_p = self.pol_deriv(s_p)
        self.sarsa_update(s, a, r, s_p, a_p)
        if d:
          break
        s, a = s_p, a_p
    return ep_per_timesteps

  def reset(self):
    self.Q = {(s,a): 0 for s in self.env.states for a in self.env.moves_d[s]}