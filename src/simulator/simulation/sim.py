"""The core algorithm for simulation trials"""

import numpy as np
import pandas as pd

from simulator.models import SimTrial
from commons.wranglers import BlobWrangler

class SimTrialRunner:
    """Takes raw inputs and simulates a single ball trajectory"""
    def __init__(self, t_initial, p_initial, v_initial, arr_windspacetime, timestep, g=9.81, m=.0456, drag_coef=0):
        """
        Parameters:
        -------
        t_initial: float
            The initial time of the sim, when the ball is hit
        p_initial: float
            The initial position of the ball
        v_initial: np.array
            The initial velocity vector of the ball
        arr_windspacetime: np.array
            The wind velocity data
        timestep: float
            The time between each row of wind speeds, and between simulation compute steps
        """
        self.t_initial = t_initial
        self.p_initial = p_initial
        self.v_initial = v_initial
        self.windspeed = arr_windspacetime
        self.timestep = timestep
        self.g = g
        self.m = m
        self.drag_coef = drag_coef

    def init_ball_trajectory(self,):
        # position
        self.ball_position = np.empty_like(self.windspeed)
        self.ball_position[:] = np.nan
        self.ball_position[self.t_initial,:] = self.p_initial
        # velocity
        self.ball_velocity = np.empty_like(self.ball_position)
        self.ball_velocity[:] = np.nan
        self.ball_velocity[self.t_initial,:] = self.v_initial

    def set_velocity_t(self, t):
        prev_v_ball = self.ball_velocity[t-1,:]
        delta_v_wind = self.windspeed[t,:] - self.windspeed[t-1,:]
        cur_v_ball = prev_v_ball + delta_v_wind + self.g*np.array(0,0,-1)
        self.ball_velocity[t,:] = cur_v_ball

    def set_position_t(self, t):
        prev_p_ball = self.ball_position[t-1,:]
        prev_v_ball = self.ball_velocity[t-1,:]
        cur_p_ball = prev_p_ball + prev_v_ball*self.timestep + 0.5*self.g*(self.timestep**2)*np.array(0,0,-1)
        self.ball_position[t,:] = cur_p_ball

    def run(self,):
        # init trajectory data
        self.init_ball_trajectory()

        # iterate till ball hits ground or windspacetime runs out
        max_t = self.windspeed.shape[0]
        t = self.t_initial + 1
        ball_hit_ground = False
        while not ball_hit_ground and t < max_t:
            self.set_position_t(t)
            self.set_velocity_t(t)
            if self.ball_position[t,2] <= 0: # hits ground (z <= 0)
                ball_hit_ground = True
            t += 1

