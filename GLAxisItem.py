from OpenGL.GL import *
from .. GLGraphicsItem import GLGraphicsItem
from . GLTextItem import GLTextItem
from ... import QtGui
from math import floor

__all__ = ['GLAxisItem']

class GLAxisItem(GLGraphicsItem):
    """
    **Bases:** :class:`GLGraphicsItem <pyqtgraph.opengl.GLGraphicsItem>`
    
    Displays three lines indicating origin and orientation of local coordinate system. 
    
    """
    
    def __init__(self, parent, size=None, axisStat = None, majorGridWidth = None, antialias=True, glOptions='translucent'):
        '''
        size: is a list of 6 floats, which sets the minimum and maximum range of all 3 axes as follows:
        [start_x, start_y, start_z, stop_x, stop_y, stop_z] or [min_x, min_y, min_z, max_x, max_y, max_z]

        axisStat: is a list of 3 bools specifying whether to draw x or y or z axis respectively

        majorGridWidth: distance between the major ticks, I want to add grid feature later so the grid spacing will
        also be specified with this feature, I'm also planning on adding minor grids and ticks feature.
        '''
        GLGraphicsItem.__init__(self)
        self.parent = parent
        if size is None:
            size = [0,0,0,100,100,100]#QtGui.QVector3D(1,1,1)

        if axisStat is None:
            axisStat = [True, True, True]

        if majorGridWidth is None:
            majorGridWidth = [5, 5, 5]

        self.antialias = antialias
        self.setSize(size=size)
        self.setAxisStat(axisStat = axisStat)
        self.setGLOptions(glOptions)
        self.setMajorGridWidth(majorGridWidth = majorGridWidth)
        self.setAxisLabel()

    def setAxisLabel(self, axis_label = None, x_label_loc = None, y_label_loc = None, z_label_loc = None, axis_label_size = None):
        """Adds axes labels."""
        '''
        axis_label: list of 3 strings for each axis
        _label_loc: a list of 3 floats (i.e. a 3D vector) specifying the location of each label
        axis_label_size: well... the size of axis label 
        the problem with this function is that when setAxisLabel() is called and 'non None' value for axis_label
        is specified the default axis labels don't go away the new labels are drawn over the default labels, but 
        specifying the label locations updates the new label locations and default labels stay put.
        '''
        _,_,_,x,y,z = self.size()
        if x_label_loc is None:
            self.x_label_loc = [x*1.05, -y/20, -z/20]
        else:
            self.x_label_loc = x_label_loc
        if y_label_loc is None:
            self.y_label_loc = [-x/20, y*1.05, -z/20]
        else:
            self.y_label_loc = y_label_loc
        if z_label_loc is None:
            self.z_label_loc = [-x/20, -y/20, z*1.05]
        else:
            self.z_label_loc = z_label_loc
        if axis_label is None:
            self.axis_label = ['X - Axis', 'Y - Axis', 'Z - Axis']
        else:
            self.axis_label = axis_label
        if axis_label_size is None:
            self.axis_label_size = 32
        else:
            self.axis_label_size = axis_label_size

        self.xLabelItem = GLTextItem(size = self.axis_label_size)
        self.xLabelItem.setX(self.x_label_loc[0])
        self.xLabelItem.setY(self.x_label_loc[1])
        self.xLabelItem.setZ(self.x_label_loc[2])
        self.xLabelItem.setText(self.axis_label[0])
        self.xLabelItem.setGLViewWidget(self.parent)
        self.parent.addItem(self.xLabelItem)
        
        self.yLabelItem = GLTextItem(size = self.axis_label_size)
        self.yLabelItem.setX(self.y_label_loc[0])
        self.yLabelItem.setY(self.y_label_loc[1])
        self.yLabelItem.setZ(self.y_label_loc[2])
        self.yLabelItem.setText(self.axis_label[1])
        self.yLabelItem.setGLViewWidget(self.parent)
        self.parent.addItem(self.yLabelItem)

        self.zLabelItem = GLTextItem(size = self.axis_label_size)
        self.zLabelItem.setX(self.z_label_loc[0])
        self.zLabelItem.setY(self.z_label_loc[1])
        self.zLabelItem.setZ(self.z_label_loc[2])
        self.zLabelItem.setText(self.axis_label[2])
        self.zLabelItem.setGLViewWidget(self.parent)
        self.parent.addItem(self.zLabelItem)
        self.update()
    
    def setSize(self, nx=None, ny=None, nz=None, px=None, py=None, pz=None, size=None):
        """
        Set the size of the axes (in its local coordinate system; this does not affect the transform)
        Arguments can be x,y,z or size=QVector3D().
        """
        if size is not None:
            nx = size[0]
            ny = size[1]
            nz = size[2]
            px = size[3]#size.x()
            py = size[4]#size.y()
            pz = size[5]#size.z()
        self.__size = [nx,ny,nz,px,py,pz]
        self.update()
        
    def size(self):
        return self.__size[:]
    
    def setAxisStat(self, x_bool = None, y_bool = None, z_bool = None, axisStat = None):
        if axisStat is not None:
            x_bool = axisStat[0]
            y_bool = axisStat[1]
            z_bool = axisStat[2]
        
        self.__axisStat = [x_bool, y_bool, z_bool]
        self.update()

    def axisStat(self):
        return self.__axisStat
    
    def setMajorGridWidth(self, major_x_grid_width = None, major_y_grid_width = None, major_z_grid_width = None, majorGridWidth = None):
        if majorGridWidth is not None:
            major_x_grid_width = majorGridWidth[0]
            major_y_grid_width = majorGridWidth[1]
            major_z_grid_width = majorGridWidth[2]

        self.__majorGridWidth = [major_x_grid_width, major_y_grid_width, major_z_grid_width]
        self.update()

    def majorGridWidth(self):
        return self.__majorGridWidth

    def paint(self):

        self.x_offset_bool = 0
        self.x_offset = 0.5*(self.size()[0]+self.size()[3])
        if (self.size()[0]<=0 and self.size()[3]>=0) or (self.size()[0]>=0 and self.size()[3]<=0):
            self.num_pX_ticks = int(round(abs((self.size()[3]-0)/self.majorGridWidth()[0]),0))
            self.num_nX_ticks = int(round(abs((0-self.size()[0])/self.majorGridWidth()[0]),0))
            self.x_offset_bool = 0
        if not((self.size()[0]<=0 and self.size()[3]>=0) or (self.size()[0]>=0 and self.size()[3]<=0)):
            self.x_half_len = 0.5*(self.size()[0]-self.size()[3])
            self.num_pX_ticks = int(round(abs((self.x_half_len)/self.majorGridWidth()[0]),0))
            self.num_nX_ticks = int(round(abs((self.x_half_len)/self.majorGridWidth()[0]),0))
            self.x_offset_bool = 1
        
        self.y_offset_bool = 0
        self.y_offset = 0.5*(self.size()[1]+self.size()[4])
        if (self.size()[1]<=0 and self.size()[4]>=0) or (self.size()[1]>=0 and self.size()[4]<=0):
            self.num_pY_ticks = int(round(abs((self.size()[4]-0)/self.majorGridWidth()[1]),0))
            self.num_nY_ticks = int(round(abs((0-self.size()[1])/self.majorGridWidth()[1]),0))
            self.y_offset_bool = 0
        if not((self.size()[1]<=0 and self.size()[4]>=0) or (self.size()[1]>=0 and self.size()[4]<=0)):
            self.y_half_len = 0.5*(self.size()[1]-self.size()[4])
            self.num_pY_ticks = int(round(abs((self.y_half_len)/self.majorGridWidth()[1]),0))
            self.num_nY_ticks = int(round(abs((self.y_half_len)/self.majorGridWidth()[1]),0))
            self.y_offset_bool = 1

        self.z_offset_bool = 0
        self.z_offset = 0.5*(self.size()[2]+self.size()[5])
        if (self.size()[2]<=0 and self.size()[5]>=0) or (self.size()[2]>=0 and self.size()[5]<=0):
            self.num_pZ_ticks = int(round(abs((self.size()[5]-0)/self.majorGridWidth()[2]),0))
            self.num_nZ_ticks = int(round(abs((0-self.size()[2])/self.majorGridWidth()[2]),0))
            self.z_offset_bool = 0

        if not((self.size()[2]<=0 and self.size()[5]>=0) or (self.size()[2]>=0 and self.size()[5]<=0)):
            self.z_half_len = 0.5*(self.size()[2]-self.size()[5])
            self.num_pZ_ticks = int(round(abs((self.z_half_len)/self.majorGridWidth()[2]),0))
            self.num_nZ_ticks = int(round(abs((self.z_half_len)/self.majorGridWidth()[2]),0))
            self.z_offset_bool = 1

        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #glEnable( GL_BLEND )
        #glEnable( GL_ALPHA_TEST )
        self.setupGLState()
        
        if self.antialias:
            glEnable(GL_LINE_SMOOTH)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
            
        
        nx,ny,nz,px,py,pz = self.size()
        x_bool, y_bool, z_bool = self.axisStat()
        
        glBegin( GL_LINES )
        if x_bool:
            #glBegin( GL_LINES )
            glColor4f(1, 0, 0, 1)  # +x is red
            glVertex3f(nx, 0, 0)
            glVertex3f(px, 0, 0)

            glColor4f(1, 1, 1, 1)
            for i in range(self.num_pX_ticks):
                glVertex3f((self.x_offset_bool*self.x_offset)+(i*self.majorGridWidth()[0]), -0.5, 0)
                glVertex3f((self.x_offset_bool*self.x_offset)+(i*self.majorGridWidth()[0]), 0.5, 0)
                glVertex3f((self.x_offset_bool*self.x_offset)+(i*self.majorGridWidth()[0]), 0, -0.5)
                glVertex3f((self.x_offset_bool*self.x_offset)+(i*self.majorGridWidth()[0]), 0, 0.5)

            for i in range(self.num_nX_ticks):
                glVertex3f((self.x_offset_bool*self.x_offset)+(-i*self.majorGridWidth()[0]), -0.5, 0)
                glVertex3f((self.x_offset_bool*self.x_offset)+(-i*self.majorGridWidth()[0]), 0.5, 0)
                glVertex3f((self.x_offset_bool*self.x_offset)+(-i*self.majorGridWidth()[0]), 0, -0.5)
                glVertex3f((self.x_offset_bool*self.x_offset)+(-i*self.majorGridWidth()[0]), 0, 0.5)
        glEnd()

        glBegin( GL_LINES )
        if y_bool:
        
            glColor4f(0, 1, 0, 1)  # +y is green
            glVertex3f(0, ny, 0)
            glVertex3f(0, py, 0)

            glColor4f(1, 1, 1, 1)
            for i in range(self.num_pY_ticks):
                glVertex3f(0.5, (self.y_offset_bool*self.y_offset)+(i*self.majorGridWidth()[1]), 0)
                glVertex3f(-0.5, (self.y_offset_bool*self.y_offset)+(i*self.majorGridWidth()[1]), 0)
                glVertex3f(0, (self.y_offset_bool*self.y_offset)+(i*self.majorGridWidth()[1]), 0.5)
                glVertex3f(0, (self.y_offset_bool*self.y_offset)+(i*self.majorGridWidth()[1]), -0.5)

            for i in range(self.num_nY_ticks):
                glVertex3f(0.5, (self.y_offset_bool*self.y_offset)+(-i*self.majorGridWidth()[1]), 0)
                glVertex3f(-0.5, (self.y_offset_bool*self.y_offset)+(-i*self.majorGridWidth()[1]), 0)
                glVertex3f(0, (self.y_offset_bool*self.y_offset)+(-i*self.majorGridWidth()[1]), 0.5)
                glVertex3f(0, (self.y_offset_bool*self.y_offset)+(-i*self.majorGridWidth()[1]), -0.5)
       
        glEnd()

        glBegin( GL_LINES )
        if z_bool:
        
            glColor4f(0, 0, 1, 1)  # +z is blue
            glVertex3f(0, 0, nz)
            glVertex3f(0, 0, pz)

            glColor4f(1, 1, 1, 1)
            for i in range(self.num_pZ_ticks):
                glVertex3f(-0.5, 0, (self.z_offset_bool*self.z_offset)+(i*self.majorGridWidth()[2]))
                glVertex3f(0.5, 0, (self.z_offset_bool*self.z_offset)+(i*self.majorGridWidth()[2]))
                glVertex3f(0, 0.5, (self.z_offset_bool*self.z_offset)+(i*self.majorGridWidth()[2]))
                glVertex3f(0, -0.5, (self.z_offset_bool*self.z_offset)+(i*self.majorGridWidth()[2]))

            for i in range(self.num_nZ_ticks):
                glVertex3f(-0.5, 0, (self.z_offset_bool*self.z_offset)+(-i*self.majorGridWidth()[2]))
                glVertex3f(0.5, 0, (self.z_offset_bool*self.z_offset)+(-i*self.majorGridWidth()[2]))
                glVertex3f(0, 0.5, (self.z_offset_bool*self.z_offset)+(-i*self.majorGridWidth()[2]))
                glVertex3f(0, -0.5, (self.z_offset_bool*self.z_offset)+(-i*self.majorGridWidth()[2]))
        glEnd()
        #glEnd()
