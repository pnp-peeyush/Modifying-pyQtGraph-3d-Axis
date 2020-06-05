from OpenGL.GL import *
from .. GLGraphicsItem import GLGraphicsItem
from ... import QtGui

class GLTextItem(GLGraphicsItem):
    def __init__(self, X=None, Y=None, Z=None, text=None, color = (255, 255, 255, 255), size = 32):
        GLGraphicsItem.__init__(self)

        self.text = text
        self.X = X
        self.Y = Y
        self.Z = Z
        self.r, self.g, self.b, self.a = color
        self.size = size
        if self.size > 64:
            raise ValueError("Value of the variable 'size' cannot be greater than 64!")

    def setGLViewWidget(self, GLViewWidget):
        self.GLViewWidget = GLViewWidget

    def setText(self, text):
        self.text = text
        self.update()

    def setX(self, X):
        self.X = X
        self.update()

    def setY(self, Y):
        self.Y = Y
        self.update()

    def setZ(self, Z):
        self.Z = Z
        self.update()

    def paint(self):
        fontObject = QtGui.QFont("Helvetica")
        fontObject.setPixelSize(self.size)
        self.GLViewWidget.qglColor(QtGui.QColor(self.r, self.g, self.b, self.a))# QtCore.Qt.white)
        self.GLViewWidget.renderText(float(self.X), float(self.Y), float(self.Z), self.text, fontObject)

def main():
    app = QtGui.QApplication([])
    w = gl.GLViewWidget()
    w.opts['distance'] = 40
    w.show()

    t = GLTextItem(X=0, Y=5, Z=10, text="Your text")
    t.setGLViewWidget(w)
    w.addItem(t)

    g = gl.GLGridItem()
    w.addItem(g)

    app.exec_()

if __name__ == '__main__':
    main()