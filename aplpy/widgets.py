from matplotlib.widgets import Widget,Button,Slider
from matplotlib import pyplot
import matplotlib as mpl
from .normalize import APLpyNormalize
import numpy as np

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

        *aplpyfigure*
            The APLPY FITSFigure host

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
            try:
                self.toolfig.canvas.set_window_title("Color Sliders for "+targetfig.canvas.manager.window.title())
            except AttributeError:
                # should try annotating instead?
                pass
            self.toolfig.subplots_adjust(top=0.9,left=0.2,right=0.9)
            mpl.rcParams['toolbar'] = tbar
        else:
            self.toolfig = toolfig
            self.toolfig.subplots_adjust(left=0.2, right=0.9)

        self.canvas = self.toolfig.canvas

        # remove ALL callbacks
        self.callbacks_dict = self.canvas.callbacks.callbacks
        for callback_type in self.callbacks_dict:
            keys = self.callbacks_dict[callback_type].keys()
            for k in keys:
                self.callbacks_dict[callback_type].pop(k)

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
                axmin = self.toolfig.add_axes([0.1,0.75,0.8,0.15])
                axmid = self.toolfig.add_axes([0.1,0.45,0.8,0.15])
                axmax = self.toolfig.add_axes([0.1,0.15,0.8,0.15])
            else:
                axmin = self.toolfig.add_axes([0.1,0.6,0.8,0.2])
                axmax = self.toolfig.add_axes([0.1,0.2,0.8,0.2])

            slmin = Slider(axmin, 'Min', self.aplpyfigure._auto_v(1e-3),
                self.aplpyfigure._auto_v(100-1e-3),
                valinit=self.aplpyfigure.image.norm.vmin,
                valfmt="%f")

            txt = slmin.valtext.get_text()
            slmin.valtext.set_text("")
            l,b,r,t = slmin.ax.bbox._bbox.get_points().ravel()
            ax = self.toolfig.add_axes((r, b, 1-r, t-b), axis_bgcolor='none',
                    frame_on=False)
            slmin.valtext = TextBox(ax,s=txt, enter_callback=slmin.set_val)

            if self.aplpyfigure.image.norm.midpoint is not None:
                midinit = self.aplpyfigure.image.norm.midpoint
                slmid = Slider(axmid, 'Mid', self.aplpyfigure._auto_v(1e-3),
                    self.aplpyfigure._auto_v(100-1e-3), valinit=midinit, slidermin=slmin,
                    valfmt="%f")
                txt = slmid.valtext.get_text()
                slmid.valtext.set_text("")
                l,b,r,t = slmid.ax.bbox._bbox.get_points().ravel()
                ax = self.toolfig.add_axes((r, b, 1-r, t-b), axis_bgcolor='none',
                    frame_on=False)
                slmid.valtext = TextBox(ax,s=txt,enter_callback=slmid.set_val)
            else:
                slmid=None

            slmax = Slider(axmax, 'Max', self.aplpyfigure._auto_v(1e-3),
                self.aplpyfigure._auto_v(100-1e-3),
                valinit=self.aplpyfigure.image.norm.vmax, slidermin=slmid,
                valfmt="%f")

            txt = slmax.valtext.get_text()
            slmax.valtext.set_text("")
            #ax = pyplot.axes([1.02,0.5,0.5,0.5])
            l,b,r,t = slmax.ax.bbox._bbox.get_points().ravel()
            ax = self.toolfig.add_axes((r, b, 1-r, t-b), axis_bgcolor='none',
                    frame_on=False)
            slmax.valtext = TextBox(ax,s=txt, enter_callback=slmax.set_val)

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


class TextBox(Widget):
    def __init__(self, ax, s='', horizontalalignment='left', enter_callback=None):
        """
        Text box!
        """

        self.value = float(s)

        self.canvas = ax.figure.canvas
        self.text = ax.text(0.025, 0.2, s,
                            fontsize=14,
                            verticalalignment='baseline',
                            horizontalalignment=horizontalalignment,
                            transform=ax.transAxes)
        self.ax = ax
        ax.set_yticks([])
        ax.set_xticks([])
    
        ax.set_navigate(False)
        self.canvas.draw()
    
        self.region = self.canvas.copy_from_bbox(ax.bbox)
    
        self._cursorpos = 0
        r = self._get_text_right()
    
        self.cursor, = ax.plot([r,r], [0.2, 0.8], transform=ax.transAxes)
        self.active = False
    
        self.redraw()
        self._cid = None

        self.enter_callback = enter_callback

    def redraw(self):
        self.ax.redraw_in_frame()
        self.canvas.blit(self.ax.bbox)
        self.canvas.draw()

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, isactive):
        self._active = bool(isactive)
        self.cursor.set_visible(self._active)
        self.redraw()

    def activate(self):
        if self._cid not in self.canvas.callbacks.callbacks['key_press_event']:
            self.old_callbacks = self.canvas.callbacks.callbacks
            
            # remove all other key bindings
            for k in self.canvas.callbacks.callbacks['key_press_event']:
                self.canvas.callbacks.callbacks['key_press_event'].pop(k)

            self._cid = self.canvas.mpl_connect('key_press_event', self.keypress)
            self.active = True

    def deactivate(self):
        if self._cid in self.canvas.callbacks.callbacks['key_press_event']:
            self.canvas.callbacks.callbacks = self.old_callbacks
            self.canvas.mpl_disconnect(self._cid)
        self.active = False

    def keypress(self, event):
        """
        Parse a keypress - only allow #'s!
        """
        #print "event.key: '%s'" % event.key
        #if event.key is not None and len(event.key)>1: return
     
        newt = t = self.text.get_text()
        if event.key == 'backspace': # simulate backspace
            if self._cursorpos == 0: return
            if len(t) > 0: 
                newt = t[:self._cursorpos-1] + t[self._cursorpos:]
            if self._cursorpos > 0:
                self._cursorpos -= 1
        elif event.key == 'left' and self._cursorpos > 0:
            self._cursorpos -= 1
        elif event.key == 'right' and self._cursorpos < len(t):
            self._cursorpos += 1
        elif event.key == 'enter':
            if self.enter_callback is not None:
                self.enter_callback(self.value)
            self.deactivate()
        elif len(event.key) > 1:
            # ignore...
            pass
        elif event.key in '0123456789':
            newt = t[:self._cursorpos] + event.key + t[self._cursorpos:]
            self._cursorpos += 1
        elif event.key == '-':
            # only allow negative at front
            if self._cursorpos == 0:
                newt = event.key + t
                self._cursorpos += 1
        elif event.key == '.':
            # do nothing if extra decimals...
            if '.' not in t:
                newt = t[:self._cursorpos] + event.key + t[self._cursorpos:]
                self._cursorpos += 1
        else:
            pass # do not allow abcdef...
     
        self.set_text(newt)
     
        r = self._get_text_right()
        self.cursor.set_xdata([r,r])
        self.redraw()

    def set_text(self, text):
        try:
            # only try to update if there's a real value
            if not(text.strip() in ('-.','.','-','')):
                self.value = float(text)
            # but always change the text
            self.text.set_text(text)
            self.redraw()
        except ValueError:
            print "error for text = ",text
            pass

    def _get_text_right(self):
        l,b,w,h = self.text.get_window_extent().bounds
        r = l+w+2
        t = b+h
        s = self.text.get_text()
        # adjust cursor position for trailing space
        numtrail = len(s)-len(s.rstrip())
        en = self.ax.get_renderer_cache().points_to_pixels(self.text.get_fontsize())/2.

        #r += numtrail*en
        r = l + self._cursorpos*np.ceil(en)
        #l,b = self.ax.transAxes.inverted().transform((l,b))
        r,t = self.ax.transAxes.inverted().transform((r,t))
        #print en,numtrail,r,l,b,t
        return r



