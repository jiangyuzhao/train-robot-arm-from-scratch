import numpy as np
import pyglet


class ArmEnv(object):
    viewer = None

    def __init__(self):
        pass

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self):
        if self.viewer is None:
            self.viewer = Viewer()
        self.viewer.render()

"""
为何要单独实现一个Viewer类？因为可视化不是环境必须提供的功能！环境只需要step和reset就可以和rl交互了
因此为了解耦合，让Viewer变成一个plugin就好了
"""


class Viewer(pyglet.window.Window):
    bar_thc = 5

    def __init__(self):
        # vsync=False to not use the monitor FPS, we can speed up training
        super(Viewer, self).__init__(width=400, height=400, resizable=False, caption='Arm', vsync=False)
        pyglet.gl.glClearColor(1, 1, 1, 1)

        self.batch = pyglet.graphics.Batch()    # display whole batch at once
        # 第一个参数表示4个顶点，第二个参数表示用多边形，之后的v2f表示位置用2个浮点数(x, y)表示，然后4个顶点因此有8个数
        # c3B是来弄颜色的, color，用3个byte表示颜色(即RGB)，*4是因为4个顶点，4个顶点都同颜色那么整个地方也就同色了
        self.point = self.batch.add(
            4, pyglet.gl.GL_QUADS, None,    # 4 corners
            ('v2f', [50, 50,                # location
                     50, 100,
                     100, 100,
                     100, 50]),
            ('c3B', (86, 109, 249) * 4))    # color
        self.arm1 = self.batch.add(
            4, pyglet.gl.GL_QUADS, None,
            ('v2f', [250, 250,                # location
                     250, 300,
                     260, 300,
                     260, 250]),
            ('c3B', (249, 86, 86) * 4,))    # color
        self.arm2 = self.batch.add(
            4, pyglet.gl.GL_QUADS, None,
            ('v2f', [100, 150,              # location
                     100, 160,
                     200, 160,
                     200, 150]), ('c3B', (249, 86, 86) * 4,))

    def render(self):
        self._update_arm()
        self.switch_to()
        self.dispatch_events()
        self.dispatch_event('on_draw')
        self.flip()

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def _update_arm(self):
        pass


if __name__ == '__main__':
    env = ArmEnv()
    while True:
        env.render()