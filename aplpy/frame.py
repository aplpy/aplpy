from decorators import auto_refresh

class Frame(object):
    
    @auto_refresh
    def __init__(self, parent):
        self._ax1 = parent._ax1
        self._figure = parent._figure

    @auto_refresh
    def set_linewidth(self, linewidth):
        '''
        Set line width of the frame

        Required arguments:

            *linewidth*:
                The linewidth to use for the frame.
        '''
        for key in self._ax1.spines:
            self._ax1.spines[key].set_linewidth(linewidth)

    @auto_refresh
    def set_color(self, color):
        '''
        Set color of the frame

        Required arguments:

            *color*:
                The color to use for the frame.
        '''
        for key in self._ax1.spines:
            self._ax1.spines[key].set_edgecolor(color)