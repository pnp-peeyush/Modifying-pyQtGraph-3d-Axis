import pyqtgraph.opengl as gl
from pyqtgraph.opengl import GLTextItem, GLAxisItem
from pyqtgraph.Qt import QtCore, QtGui

def main():
    app = QtGui.QApplication([])
    w = gl.GLViewWidget()
    w.opts['distance'] = 40
    w.setBackgroundColor(0.2)
    w.show()

    t = GLTextItem(X=0, Y=5, Z=10, text="Your text")
    t.setText('kjwdc')
    t.setGLViewWidget(w)
    w.addItem(t)

    ax = GLAxisItem(w)
    ax.setAxisLabel(axis_label=['Chamber Pressure (Pc)', '% Fuel fraction', 'Specific Impulse (Isp)'], x_label_loc=[70,-20,-20])
    w.addItem(ax)

    '''g = gl.GLGridItem()
    w.addItem(g)'''

    app.exec_()

if __name__ == '__main__':
    main()