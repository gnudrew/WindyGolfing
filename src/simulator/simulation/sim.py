"""The core algorithm for simulation trials"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint

from simulator.models import SimTrial
from commons.wranglers import BlobWrangler

class SimTrialRunner:
    """Takes raw inputs and simulates a single ball trajectory using physics"""
    def __init__(self, 
        t_initial, 
        p_initial, 
        v_initial, 
        arr_windspacetime, 
        timestep, 
        g=9.81, 
        m=.0456, 
        drag_coef=0,
        verbosity=1,
    ):
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
            delta_t, the time interval between each row of wind speeds, and between simulation compute steps
        """
        print(f'[SimTrialRunner] Preparing parameters...')
        self.t_initial = t_initial
        self.p_initial = p_initial
        self.v_initial = v_initial
        self.windspeed = arr_windspacetime
        self.timestep = timestep
        self.g = g
        self.m = m
        self.drag_coef = drag_coef
        self.verbosity = verbosity
        print(f'[SimTrialRunner] OK.')

        if self.verbosity >= 1:
            print(f'[SimTrialRunner] ====================================')
            print(f'[SimTrialRunner] Run parameters are:')
            print(f'  >> t_initial    = {self.t_initial}')
            print(f'  >> p_initial    = {self.p_initial}')
            print(f'  >> v_initial    = {self.v_initial}')
            print(f'  >> windspeed_id = {""}')
            print(f'  >> timestep     = {self.timestep}')
            print(f'  >> g            = {self.g}')
            print(f'  >> m            = {self.m}')
            print(f'  >> drag_coef    = {self.drag_coef}')
            print(f'  >> verbosity    = {self.verbosity}')
            print(f'[SimTrialRunner] ====================================')

    def init_ball_trajectory(self,):
        if self.verbosity >= 1:
            print(f'[SimTrialRunner] Initializing ball trajectory...')
        # position
        self.ball_position = np.empty_like(self.windspeed)
        self.ball_position[:] = np.nan
        self.ball_position[self.t_initial,:] = self.p_initial
        # velocity
        self.ball_velocity = np.empty_like(self.ball_position)
        self.ball_velocity[:] = np.nan
        self.ball_velocity[self.t_initial,:] = self.v_initial

        if self.verbosity >= 1:
            print(f'[SimTrialRunner] Initialized.')

    def set_velocity_t(self, t):
        if self.verbosity >= 2:
            print(f'[SimTrialRunner] Setting next ball velocity...')

        prev_v = self.ball_velocity[t-1,:]
        dv_wind = self.windspeed[t,:] - self.windspeed[t-1,:]
        cur_v = prev_v + dv_wind + self.g*np.array([0,0,-1])*self.timestep # a = dv/dt --> dv = dv_wind + dv_grav = dv_wind + a*dt --> vf = vi + dv_wind + a*dt
        self.ball_velocity[t,:] = cur_v

        if self.verbosity >= 2:
            print(f'[SimTrialRunner] set: {prev_v} -> {cur_v}')

    def set_position_t(self, t):
        if self.verbosity >= 2:
            print(f'[SimTrialRunner] setting next ball position...')

        prev_p = self.ball_position[t-1,:] # position
        prev_v = self.ball_velocity[t-1,:] # velocity
        cur_p = prev_p + prev_v*self.timestep # v = dx/dt --> dx = v*dt --> xf = xi + dx = xi + v*dt
        self.ball_position[t,:] = cur_p

        if self.verbosity >= 2:
            print(f'[SimTrialRunner] set.')

    def run(self,):
        if self.verbosity >= 1:
            print(f'[SimTrialRunner] Running trial...')
        # init trajectory data
        self.init_ball_trajectory()

        # iterate till ball hits ground or windspacetime runs out
        max_t = self.windspeed.shape[0]
        t = self.t_initial + 1
        ball_hit_ground = False
        while not ball_hit_ground and t < max_t:
            if self.verbosity >= 2:
                print(f'[SimTrialRunner] Calculating @ timestep={t}.')

            self.set_position_t(t)
            self.set_velocity_t(t)
            if self.ball_position[t,2] <= 0: # hits ground (z <= 0)
                ball_hit_ground = True
            t += 1

        if self.verbosity >= 1:
            print(f'[SimTrialRunner] ====================================')
            print(f'[SimTrialRunner] Completed Run.')
            print(f'[SimTrialRunner]  >> Ball hit ground?.. {"YES" if ball_hit_ground else "NO"}.')
            print(f'[SimTrialRunner]  >> Trajectory duration = {t*self.timestep}s.')
            print(f'[SimTrialRunner] Fin.')

        # remove trailing nans --> assume no nans exist in the main trajectory
        self.ball_position = self.ball_position[0:t, :]

        return self.ball_position

    def _plot_arr(self, arr):
        plt.plot(arr)
        plt.show

    def plotx(self,):
        x = self.ball_position[:,0]
        self._plot_arr(x)
    
    def ploty(self,):
        y = self.ball_position[:,1]
        self._plot_arr(y)

    def plotz(self,):
        z = self.ball_position[:,2]
        self._plot_arr(z)