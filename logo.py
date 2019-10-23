import numpy as np
import matplotlib.pyplot as plt
from subprocess import check_call

circle_color = 'w'
sinc_color = '#5f1904'
bgcolor = (1., 1., 1., 0.)
extent = 6
times = np.linspace(-extent, extent, 1000, endpoint=True)
x = (extent * 1.2) * np.sinc(times)
fig = plt.figure(figsize=(5, 5))
fig.set_facecolor(bgcolor)
ax = plt.axes([0, 0, 1, 1])
circle = plt.Circle((0, 0), extent, color=circle_color, zorder=2)
ax.add_artist(circle)
ax.axis('off')
# ax.fill_between(times, x * 0.1, x, color=sinc_color, zorder=3)
ax.plot(times, x - 2.0, color=sinc_color, zorder=3, lw=10)
ax.set(xlim=[-extent, extent], ylim=[-extent, extent])
fig.savefig('logo.png', transparent=True)
check_call([
    'convert',
    '-resize', 'x16',
    '-gravity', 'center',
    '-crop',
    '16x16+0+0',
    'logo.png',
    '-background', 'transparent',
    'content/extra/favicon.ico'
])
