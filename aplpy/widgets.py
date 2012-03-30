from matplotlib.widgets import Widget,Button,Slider
from matplotlib import pyplot
import matplotlib as mpl
from .normalize import APLpyNormalize

class ColorSliders(Widget):
    """
    A tool to adjust to subplot params of a :class:`matplotlib.figure.Figure`
    """
    def __init__(self, targetfig, aplpyfigure=None, toolfig=None):
        """

        Parameters
        ----------
        *targetfig*
            The figure instance to adjust

        *toolfig*
            The figure instance to embed the subplot tool into. If
            None, a default figure will be created. If you are using
            this from the GUI
        """

        self.targetfig = targetfig

        if toolfig is None:
            tbar = mpl.rcParams['toolbar'] # turn off the navigation toolbar for the toolfig
            mpl.rcParams['toolbar'] = 'None'
            self.toolfig = pyplot.figure(figsize=(6,3))
            self.toolfig.canvas.set_window_title("Color Sliders for "+targetfig.canvas.manager.window.title())
            self.toolfig.subplots_adjust(top=0.9,left=0.2,right=0.9)
            mpl.rcParams['toolbar'] = tbar
        else:
            self.toolfig = toolfig
            self.toolfig.subplots_adjust(left=0.2, right=0.9)


        bax = self.toolfig.add_axes([0.8, 0.05, 0.15, 0.075])
        self.buttonreset = Button(bax, 'Reset')

        self.aplpyfigure = aplpyfigure

        self.set_sliders()

        def reset(event):
            thisdrawon = self.drawon

            self.drawon = False

            # store the drawon state of each slider
            bs = []
            for slider in self.sliders:
                bs.append(slider.drawon)
                slider.drawon = False

            # reset the slider to the initial position
            for slider in self.sliders:
                slider.reset()

            # reset drawon
            for slider, b in zip(self.sliders, bs):
                slider.drawon = b

            # draw the canvas
            self.drawon = thisdrawon
            if self.drawon:
                self.toolfig.canvas.draw()
                self.targetfig.canvas.draw()


        # during reset there can be a temporary invalid state
        # depending on the order of the reset so we turn off
        # validation for the resetting
        validate = self.toolfig.subplotpars.validate
        self.toolfig.subplotpars.validate = False
        self.buttonreset.on_clicked(reset)
        self.toolfig.subplotpars.validate = validate


    def clear_sliders(self):
        """
        Get rid of the sliders...
        """
        try:
            for sl in self.sliders:
                sl.ax.remove()
        except NotImplementedError:
            for sl in self.sliders:
                self.toolfig.delaxes(sl.ax)

    def set_sliders(self):
        if self.aplpyfigure.image:
            if self.aplpyfigure.image.norm.midpoint is not None:
                axmin = self.toolfig.add_axes([0.1,0.7,0.8,0.2])
                axmid = self.toolfig.add_axes([0.1,0.4,0.8,0.2])
                axmax = self.toolfig.add_axes([0.1,0.1,0.8,0.2])
            else:
                axmin = self.toolfig.add_axes([0.1,0.6,0.8,0.3])
                axmax = self.toolfig.add_axes([0.1,0.2,0.8,0.3])

            slmin = Slider(axmin, 'Min', self.aplpyfigure._auto_v(1e-3),
                self.aplpyfigure._auto_v(100-1e-3), valinit=self.aplpyfigure.image.norm.vmin)

            if self.aplpyfigure.image.norm.midpoint is not None:
                midinit = self.aplpyfigure.image.norm.midpoint
                slmid = Slider(axmid, 'Mid', self.aplpyfigure._auto_v(1e-3),
                    self.aplpyfigure._auto_v(100-1e-3), valinit=midinit, slidermin=slmin)
            else:
                slmid=None

            slmax = Slider(axmax, 'Max', self.aplpyfigure._auto_v(1e-3),
                self.aplpyfigure._auto_v(100-1e-3), valinit=self.aplpyfigure.image.norm.vmax, slidermin=slmid)

            if slmid is None:
                slmin.slidermax = slmax
                slmax.slidermin = slmin
            else:
                slmid.slidermax = slmax
                slmin.slidermax = slmid

            stretch = self.aplpyfigure.image.norm.stretch
            exponent = self.aplpyfigure.image.norm.exponent

            def update(value):
                midval = slmid.val if slmid is not None else None
                self.aplpyfigure.image.set_norm(APLpyNormalize(stretch=stretch, 
                    exponent=exponent, vmin=slmin.val, vmid=midval, vmax=slmax.val))
                self.aplpyfigure.refresh()
                if hasattr(self.aplpyfigure, 'colorbar'):
                    self.aplpyfigure.colorbar.update()

            slmin.on_changed(update)
            if slmid is not None: slmid.on_changed(update)
            slmax.on_changed(update)

            if slmid is None:
                self.sliders = [slmin,slmax]
            else:
                self.sliders = [slmin,slmid,slmax]

