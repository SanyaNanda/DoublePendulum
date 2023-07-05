from flask import Flask, render_template, url_for, request, redirect
import code1
from matplotlib import animation, rc
import scipy.integrate as integrate
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#import base64
#import io
#import random
from flask import Response
#import ffmpeg
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#from matplotlib.figure import Figure
#from IPython.display import HTML


app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/SeeitSwing!',methods=['POST'])
def predict():
        m1=request.form['mass1']
        m2=request.form['mass2']
        l1=request.form['len1']
        l2=request.form['len2']
        t1=request.form['theta1']
        t2=request.form['theta2']
        g=request.form['grav']
        m1=float(m1)
        m2=float(m2)
        l1=float(l1)
        l2=float(l2)
        t1=float(t1)
        t2=float(t2)
        g=float(g)
        th=[]
        th.append(t1)
        th.append(t2)
        d=code1.DoublePendulum(m1,m2,l1,l2,g,th)
        time1=d.time()
        s1=d.states()
        y = integrate.odeint(d.derivs,s1,time1)
        x1=d.x1(y)
        y1=d.y1(y)
        x2=d.x2(y,x1)
        y2=d.y2(y,y1)
        k=d.K(y)
        v=d.V(y)

        fig = plt.figure()
        ax = fig.add_subplot(111, autoscale_on=False, xlim=(-5, 5), ylim=(-5, 5))
        ax.grid()
        line1, = ax.plot([], [], 'o-', lw=2)
        time_template = 'time = %.1fs'
        k_template = 'K.E = %.2fJ'
        v_template = 'P.E = %.2fJ'
        time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
        k_text = ax.text(0.25, 0.9, '', transform=ax.transAxes)
        v_text = ax.text(0.45, 0.9, '', transform=ax.transAxes)

        def init():
            line1.set_data([], [])
            time_text.set_text('')
            k_text.set_text('')
            v_text.set_text('')
            return line1, time_text,k_text,v_text


        def animate(i):
            thisx = [0, x1[i], x2[i]]
            thisy = [0, y1[i], y2[i]]
            line1.set_data(thisx, thisy)
            time_text.set_text(time_template % (i*0.05))
            k_text.set_text(k_template % (k[i]))
            v_text.set_text(v_template % (v[i]))
            return line1, time_text, k_text, v_text

        #Writer = animation.FFMpegWriter(fps=20, metadata=dict(artist='Me'), bitrate=1800)
        #plt.rcParams["animation.html"] = "html5"
        #rc('animation', html='html5')
        plt.title('Motion of The Double Pendulum')
        #animation.writer(ffmpeg)
        #ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y)),interval=25, blit=True, init_func=init)
        anim = animation.FuncAnimation(fig, animate, init_func=init, frames=400, interval=20, blit=True)

        # Writer = animation.writers['ffmpeg']
        # writer = Writer(fps=1000/interval, metadata=self.params, bitrate=1)
        # ani.save(writer=writer)

        with open("templates/myvideo.html", "w") as f:
            print(anim.to_html5_video())#, file=f)

        return render_template("myvideo.html" )

        # def animatee(i):
        #     a = [0, y[:,0][i],y[:,2][i]]
        #     line2.set_data(a)
        # ani1 = animation.FuncAnimation(fig, animatee, np.arange(1, len(y)),interval=25, blit=True, init_func=init)

@app.route('/GraphPlot',methods=['POST'])
def predict1():
        m1=request.form['mass1']
        m2=request.form['mass2']
        l1=request.form['len1']
        l2=request.form['len2']
        t1=request.form['theta1']
        t2=request.form['theta2']
        g=request.form['grav']
        m1=float(m1)
        m2=float(m2)
        l1=float(l1)
        l2=float(l2)
        t1=float(t1)
        t2=float(t2)
        g=float(g)
        th=[]
        th.append(t1)
        th.append(t2)
        d=code1.DoublePendulum(m1,m2,l1,l2,g,th)
        time1=d.time()
        s1=d.states()
        y = integrate.odeint(d.derivs,s1,time1)
        x1=d.x1(y)
        y1=d.y1(y)
        x2=d.x2(y,x1)
        y2=d.y2(y,y1)
        k=d.K(y)
        v=d.V(y)

        fig = plt.figure(figsize = (12,8))
        ax = fig.add_subplot(111, autoscale_on=True)    # The big subplot
        ax1 = fig.add_subplot(211, autoscale_on=True)
        ax2 = fig.add_subplot(212, autoscale_on=True)
        ax1.set_title('Energy vs Time')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Energy')
        ax1.plot(time1,k,label = "Kinetic Energy")
        ax1.plot(time1,v,label = "Potential Energy")
        ax1.legend()

        ax2.set_title('Position vs angle')
        ax2.set_xlabel('Angle')
        ax2.set_ylabel('Position')
        ax2.plot(y[:, 0],x1,label = "Position of the upper pendulum wrt theta1")
        ax2.plot(y[:, 2],x2, label = "Position of the lower pendulum wrt theta2")
        ax2.legend()
        plt.autoscale()
        plt.tight_layout()
        plt.savefig('static/'+'img2'+'.png')

        return render_template("success.html",name = 'new_plot',url2 ='../static/'+'img2'+'.png' )



#@app.route('/plot.gif')
# @app.route('/success')
# def plot_png():
#     output = io.BytesIO()
#     FigureCanvas(predict(ani)).print_gif(output)
#     return Response(output.getvalue(), mimetype='image/gif')
#     return render_template('success.html')


        # fig = plt.figure()
        # ax = fig.add_subplot(111, autoscale_on=False, xlim=(-5, 5), ylim=(-5, 5))
        # ax.grid()
        # line1, = ax.plot([], [], 'o-', lw=2)
        # time_template = 'time = %.1fs'
        # k_template = 'K.E = %.2fJ'
        # v_template = 'P.E = %.2fJ'
        # time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
        # k_text = ax.text(0.25, 0.9, '', transform=ax.transAxes)
        # v_text = ax.text(0.45, 0.9, '', transform=ax.transAxes)


        # def init():
        #     line1.set_data([], [])
        #     time_text.set_text('')
        #     k_text.set_text('')
        #     v_text.set_text('')
        #     return line1, time_text,k_text,v_text
        #
        #
        # def animate(i):
        #     thisx = [0, x1[i], x2[i]]
        #     thisy = [0, y1[i], y2[i]]
        #     line1.set_data(thisx, thisy)
        #     time_text.set_text(time_template % (i*0.05))
        #     k_text.set_text(k_template % (k[i]))
        #     v_text.set_text(v_template % (v[i]))
        #     return line1, time_text, k_text, v_text
        #
        # ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y)),interval=25, blit=True, init_func=init)
        # #ani.save('double_pendulum2.gif', fps=15)
        # tmpfile = BytesIO()
        # fig.savefig(tmpfile, format='png')
        # encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        # html = 'Some html head' + '<img src=\'data:image/png;base64,{}\'>'.format(encoded) + 'Some more html'
        #
        # with open('home.html','w') as f:
        #     f.write(html)
        #mpld3.show()
        #plt.plot(k,time1)
        #mpld3.show()
        #return redirect(url_for('home'))
        #return redirect(url_for('success', name = output))


if __name__ == '__main__':
    app.run(debug=False)
