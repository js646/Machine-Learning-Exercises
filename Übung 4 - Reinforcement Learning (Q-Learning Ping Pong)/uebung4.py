# Julian Schlee 1821112
import sys
import time
import math
try:
    import numpy as np
except:
    print("ERROR: Numpy not installed properly.")
    sys.exit()
try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print("ERROR: PyOpenGL not installed properly.")
    sys.exit()

'''
INSTALLATION:
-----------------------------------------
unter anaconda (python 3.6):
    conda install numpy
    conda install freeglut
    conda install pyopengl
    conda install pyopengl-accelerate

(bei fehlenden Bibliotheken googeln)

Ausführung:
    start anaconda prompt
    navigiere in den Game Ordner
    tippe: python A5.py
-----------------------------------------
'''


class GameGL(object):
    config = None

    def __init__(self, config = None):
        self.config = config
    '''
    Is needed for the OpenGL-Library because standard strings are not allowed.
    '''
    def toCString(self, string):
        return bytes(string, "ascii")


# ----------------------------------------------------------
# Zustand aus Koordinaten berechnen
def get_state(koordinaten, max_werte):
    # Wert von xV und yV auf 0 setzen falls negativ; auf 1 falls positiv
    for i in range(3, 5):
        if koordinaten[i] < 0:
            koordinaten[i] = 0
        elif koordinaten[i] > 0:
            koordinaten[i] = 1

    s = koordinaten[0]
    for i in range(1, len(koordinaten)):
        s = s * max_werte[i] + koordinaten[i]
    return s
# ----------------------------------------------------------


class BasicGame(GameGL):

    windowName = "PingPong"
    # 30px
    pixelSize = 30

    xBall      = 5
    yBall      = 6
    xSchlaeger = 5
    xV         = 1
    yV         = 1
    score      = 0
    # ----------------------------------------------------------
    max_values = [12, 12, 10, 2, 2]
    qtable = np.random.uniform(low=0, high=1.0, size=(5760, 3))  # 12 * 12 * 10 * 2 * 2 = 5760 states
    state = get_state([xBall, yBall, xSchlaeger, xV, yV], max_values)
    learning_rate = 0.2
    discount_factor = 0.90
    epsilon = 0.1
    episode = 1
    # ----------------------------------------------------------

    def __init__(self, name, width = 360, height = 360):
        super
        self.windowName = name
        self.width      = width
        self.height     = height
        # ----------------------------------------------------------
        ''' Test auf eindeutige Abbildung von get_state
        states = []
        i = 0
        for x in range(0, 12):
            for y in range(0, 12):
                for xs in range(0, 10):
                    for xv in range(0, 2):
                        for yv in range(0, 2):
                            states.append(get_state([x, y, xs, xv, yv], self.max_values))
                            i += 1
        print("states: "+str(len(states)))
        print(str(states))
        '''
        # ----------------------------------------------------------

    def keyboard(self, key, x, y):
        # ESC = \x1w
        if key == b'\x1b':
            sys.exit(0)

    def display(self):
        # clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # reset position
        glLoadIdentity()
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.width, 0.0, self.height, 0.0, 1.0)
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()

        # ----------------------------------------------------------
        # epsilon-greedy Aktionsauswahl
        if np.random.uniform(0.0, 1.0) < self.epsilon:
            selected_action = np.random.default_rng().choice([0, 1, 2])
        else:
            selected_action = np.argmax(self.qtable[self.state])

        if selected_action == 0:
            action = -1
        elif selected_action == 1:
            action = 0
        elif selected_action == 2:
            action = 1

        reward = 0
        # ----------------------------------------------------------

        #action = 2.0 * np.random.random() - 1.0
        if action < -0.3:
            self.xSchlaeger -= 1
        if action > 0.3:
            self.xSchlaeger += 1
        # don't allow puncher to leave the pitch
        if self.xSchlaeger < 0:
            self.xSchlaeger = 0
        if self.xSchlaeger > 9:
            self.xSchlaeger = 9

        self.xBall += self.xV
        self.yBall += self.yV
        # change direction of ball if it's at wall
        if self.xBall > 10 or self.xBall < 1:
            self.xV = -self.xV
        if self.yBall > 10 or self.yBall < 1:
            self.yV = -self.yV
        # check whether ball on bottom line
        if self.yBall == 0:
            # check whether ball is at position of player
            if (self.xSchlaeger == self.xBall 
                    or self.xSchlaeger == self.xBall -1
                    or self.xSchlaeger == self.xBall -2):
                # ----------------------------------------------------------
                self.score += 1
                print("positive reward for episode "+str(self.episode))
                print("current score: " + str(self.score)+"/"+str(self.episode))
                reward = 1
                self.episode += 1
            else:
                print("negative reward for episode "+str(self.episode))
                print("current score: " + str(self.score) + "/" + str(self.episode))
                reward = -1
                self.episode += 1
                # ----------------------------------------------------------

        # ----------------------------------------------------------
        # Q-Update
        new_coordinates = [self.xBall, self.yBall, self.xSchlaeger, self.xV, self.yV]
        new_state = get_state(new_coordinates, self.max_values)

        old_q = self.qtable[self.state][selected_action]
        max_future_q = np.max(self.qtable[new_state])
        new_q = old_q + (self.learning_rate * (reward + (self.discount_factor * max_future_q) - old_q))

        self.qtable[self.state][selected_action] = new_q
        self.state = new_state
        # ----------------------------------------------------------

        # repaint
        self.drawBall()
        self.drawComputer()

        # timeout of 100 milliseconds
        time.sleep(0.1)
        
        glutSwapBuffers()
    
    def start(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(self.toCString(self.windowName))
        #self.init()
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.onResize)
        glutIdleFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        glutMainLoop() 
    
    def updateSize(self):
        self.width  = glutGet(GLUT_WINDOW_WIDTH)
        self.height = glutGet(GLUT_WINDOW_HEIGHT)
    
    def onResize(self, width, height):
        self.width  = width
        self.height = height
    
    def drawBall(self, width = 1, height = 1, x = 5, y = 6, color = (0.0, 1.0, 0.0)):
        x = self.xBall
        y = self.yBall
        xPos = x * self.pixelSize
        yPos = y * self.pixelSize
        # set color
        glColor3f(color[0], color[1], color[2])
        # start drawing a rectangle
        glBegin(GL_QUADS)
        # bottom left point
        glVertex2f(xPos, yPos)
        # bottom right point
        glVertex2f(xPos + (self.pixelSize * width), yPos)
        # top right point
        glVertex2f(xPos + (self.pixelSize * width), yPos + (self.pixelSize * height))
        # top left point
        glVertex2f(xPos, yPos + (self.pixelSize * height))
        glEnd()
    
    def drawComputer(self, width = 3, height = 1, x = 0, y = 0, color = (1.0, 0.0, 0.0)):
        x = self.xSchlaeger
        xPos = x * self.pixelSize
        # set a bit away from bottom
        yPos = y * self.pixelSize# + (self.pixelSize * height / 2)
        # set color
        glColor3f(color[0], color[1], color[2])
        # start drawing a rectangle
        glBegin(GL_QUADS)
        # bottom left point
        glVertex2f(xPos, yPos)
        # bottom right point
        glVertex2f(xPos + (self.pixelSize * width), yPos)
        # top right point
        glVertex2f(xPos + (self.pixelSize * width), yPos + (self.pixelSize * height / 4))
        # top left point
        glVertex2f(xPos, yPos + (self.pixelSize * height / 4))
        glEnd()


if __name__ == '__main__':
    game = BasicGame("PingPong")
    game.start()