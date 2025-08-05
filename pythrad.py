

#Project Developed by SAHAN (BE CSE ICB)
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import time
import serial
import keyboard
ser=serial.Serial('COM3',baudrate=9600,bytesize=8,parity='N',stopbits=1,timeout=2)

fig=plt.figure(facecolor='k')
fig.canvas.toolbar.pack_forget()
fig.canvas.manager.set_window_title('Ultrasonic Radar')
mgn=plt.get_current_fig_manager()
mgn.window.state('normal')

ax=fig.add_subplot(1,1,1,polar=True,facecolor='#006b78')
ax.tick_params(axis='both',colors='w')
r_max=200
ax.set_ylim([0.0,r_max])
ax.set_xlim([0.0,np.pi])
ax.set_position([-0.05,-0.05,1.1,1.05])
ax.set_rticks(np.linspace(0.0,180,10))
angles=np.arange(0,181,1)
theta=angles*(np.pi/180)

pols,=ax.plot([],linestyle='',marker='o',markerfacecolor='r',markeredgecolor='w',markeredgewidth=1.0,markersize=4.0,alpha=0.5)
line1,=ax.plot([],color='w',linewidth=0.01)
#fig.canvas.draw()
dists=np.ones((len(angles),))
axbackground=fig.canvas.copy_from_bbox(ax.bbox)


while True:
    try:
        data=ser.readline()
        decoded=data.decode()
        data=(decoded.replace('\r',''))
        vals=[float(ii)for ii in data.split(',')]
        if len(vals)<2.0:
            continue
        angle,distance=vals
        #print(angle,distance)
        dists[int(angle)]=distance
        pols.set_data(theta,dists)
        fig.canvas.restore_region(axbackground)
        ax.draw_artist(pols)

        line1.set_data(np.repeat((angle*(np.pi/180)),2),np.linspace(0.0,r_max,2))
        ax.draw_artist(line1)
        fig.canvas.blit(ax.bbox)
        fig.canvas.flush_events()

        if keyboard.is_pressed('q'):
            plt.close('all')
            print("User need to quit the application")
            break
            
                
    except KeyboardInterrupt:
        print('Keyboard Interrupt')
        break



exit()

