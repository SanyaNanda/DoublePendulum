import numpy as np
from numpy import cos,sin
import matplotlib.pyplot as plt
import scipy.integrate as integrate
#import matplotlib.animation as animation


class DoublePendulum():
    def __init__(self,M1,M2,L1,L2,g,theta=[]):
        self.M1=M1
        self.M2=M2
        self.L1=L1
        self.L2=L2
        self.g=g
        self.theta=theta

    def time(self):
        dt = 0.05
        t = np.arange(0.0, 20, dt)
        return t

    def states(self):
        th1=self.theta[0]
        th2=self.theta[1]
        w1=0
        w2=0
        state = np.radians([th1, w1, th2, w2])
        return state

    def derivs(self,state,t):

        dydx = np.zeros_like(state)
        dydx[0] = state[1]

        del_ = state[2] - state[0]

        den1 = (self.M1 + self.M2)*self.L1 - self.M2*self.L1*cos(del_)*cos(del_)
        dydx[1] = (self.M2*self.L1*state[1]*state[1]*sin(del_)*cos(del_) +
                   self.M2*self.g*sin(state[2])*cos(del_) +
                   self.M2*self.L2*state[3]*state[3]*sin(del_) -
                   (self.M1 + self.M2)*self.g*sin(state[0]))/den1

        dydx[2] = state[3]

        den2 = (self.L2/self.L1)*den1
        dydx[3] = (-self.M2*self.L2*state[3]*state[3]*sin(del_)*cos(del_) +
                   (self.M1 + self.M2)*self.g*sin(state[0])*cos(del_) -
                   (self.M1 + self.M2)*self.L1*state[1]*state[1]*sin(del_) -
                   (self.M1 + self.M2)*self.g*sin(state[2]))/den2

        return dydx

    def x1(self,y):
        x1 = self.L1*sin(y[:, 0])
        return x1
    def y1(self,y):
        y1 = -self.L1*cos(y[:, 0])
        return y1
    def x2(self,y,x1):
        x2 = self.L2*sin(y[:, 2]) + x1
        return x2
    def y2(self,y,y1):
        y2 = -self.L2*cos(y[:, 2]) + y1
        return y2
    def V(self,y):
        V=(self.M1 + self.M2)*(self.L1)*self.g*cos(y[:,0]) + self.M2*self.g*self.L2*cos(y[:,2])
        return V

    def K(self,y):
        K=(self.M1/2+self.M2/2)*(self.L1**2)*(y[:,1]**2) + (self.M2/2)*(self.L2**2)*(y[:,3]**2)+ (self.M2)*self.L1*self.L2*y[:,1]*y[:,3]*cos(y[:,0]-y[:,2])
        return K

# fig = plt.figure()
# ax = fig.add_subplot(111, autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2))
# ax.grid()
# line1, = ax.plot([], [], 'o-', lw=2)
# time_template = 'time = %.1fs'
# k_template = 'K.E = %.2fJ'
# v_template = 'P.E = %.2fJ'
# time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
# k_text = ax.text(0.25, 0.9, '', transform=ax.transAxes)
# v_text = ax.text(0.45, 0.9, '', transform=ax.transAxes)
#
#
# def init():
#     line1.set_data([], [])
#     time_text.set_text('')
#     k_text.set_text('')
#     v_text.set_text('')
#     return line1, time_text
#
#
# def animate(i):
#     thisx = [0, x1[i], x2[i]]
#     thisy = [0, y1[i], y2[i]]
#     line1.set_data(thisx, thisy)
#     time_text.set_text(time_template % (i*0.05))
#     k_text.set_text(k_template % (k[i]))
#     v_text.set_text(v_template % (v[i]))
#     return line1, time_text

# ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y)),
#                               interval=25, blit=True, init_func=init)
# ani.save('static/double_pendulum2.gif', fps=15)
