from __future__ import absolute_import, print_function, division

from matplotlib.contour import ContourSet
from matplotlib.collections import RegularPolyCollection, \
    PatchCollection, CircleCollection, LineCollection

from .regions import ArtistCollection
from .decorators import auto_refresh


class Layers(object):

    def __init__(self):
        pass

    def _layer_type(self, layer):
        if isinstance(self._layers[layer], ContourSet):
            return 'contour'
        elif isinstance(self._layers[layer], RegularPolyCollection):
            return 'collection'
        elif isinstance(self._layers[layer], PatchCollection):
            return 'collection'
        elif isinstance(self._layers[layer], CircleCollection):
            return 'collection'
        elif isinstance(self._layers[layer], LineCollection):
            return 'collection'
        elif isinstance(self._layers[layer], ArtistCollection):
            return 'collection'
        elif hasattr(self._layers[layer], 'remove') and hasattr(self._layers[layer], 'get_visible') and hasattr(self._layers[layer], 'set_visible'):
            return 'collection'
        else:
            raise Exception("Unknown layer type: " + \
                str(type(self._layers[layer])))

    def _initialize_layers(self):

        self._layers = {}
        self._contour_counter = 0
        self._scatter_counter = 0
        self._circle_counter = 0
        self._ellipse_counter = 0
        self._rectangle_counter = 0
        self._linelist_counter = 0
        self._region_counter = 0
        self._label_counter = 0
        self._poly_counter = 0

    def list_layers(self):
        '''
        Print a list of layers to standard output.
        '''

        layers_list = []

        for layer in self._layers:

            layer_type = self._layer_type(layer)

            if layer_type == 'contour':
                visible = self._layers[layer].collections[0].get_visible()
            elif layer_type == 'collection':
                visible = self._layers[layer].get_visible()

            layers_list.append({'name': layer, 'visible': visible})

        n_layers = len(layers_list)
        if n_layers == 0:
            print("\n  There are no layers in this figure")
        else:
            if n_layers == 1:
                print("\n  There is one layer in this figure:\n")
            else:
                print("\n  There are " + str(n_layers) + \
                    " layers in this figure:\n")
            for layer in layers_list:
                if layer['visible']:
                    print("   -> " + layer['name'])
                else:
                    print("   -> " + layer['name'] + " (hidden)")

    @auto_refresh
    def remove_layer(self, layer, raise_exception=True):
        '''
        Remove a layer.

        Parameters
        ----------
        layer : str
            The name of the layer to remove
        '''

        if layer in self._layers:

            layer_type = self._layer_type(layer)

            if layer_type == 'contour':
                for contour in self._layers[layer].collections:
                    contour.remove()
                self._layers.pop(layer)
            elif layer_type == 'collection':
                self._layers[layer].remove()
                self._layers.pop(layer)
                if (layer + '_txt') in self._layers:
                    self._layers[layer + '_txt'].remove()
                    self._layers.pop(layer + '_txt')

        else:

            if raise_exception:
                raise Exception("Layer " + layer + " does not exist")

    @auto_refresh
    def hide_layer(self, layer, raise_exception=True):
        '''
        Hide a layer.

        This differs from remove_layer in that if a layer is hidden
        it can be shown again using show_layer.

        Parameters
        ----------
        layer : str
            The name of the layer to hide
        '''
        if layer in self._layers:

            layer_type = self._layer_type(layer)

            if layer_type == 'contour':
                for contour in self._layers[layer].collections:
                    contour.set_visible(False)
            elif layer_type == 'collection':
                self._layers[layer].set_visible(False)

        else:

            if raise_exception:
                raise Exception("Layer " + layer + " does not exist")

    @auto_refresh
    def show_layer(self, layer, raise_exception=True):
        '''
        Show a layer.

        This shows a layer previously hidden with hide_layer

        Parameters
        ----------
        layer : str
            The name of the layer to show
        '''
        if layer in self._layers:

            layer_type = self._layer_type(layer)

            if layer_type == 'contour':
                for contour in self._layers[layer].collections:
                    contour.set_visible(True)
            elif layer_type == 'collection':
                self._layers[layer].set_visible(True)

        else:
            if raise_exception:
                raise Exception("Layer " + layer + " does not exist")

    def get_layer(self, layer, raise_exception=True):
        '''
        Return a layer object.

        Parameters
        ----------
        layer : str
            The name of the layer to return
        '''
        if layer in self._layers:
            return self._layers[layer]
        else:
            if raise_exception:
                raise Exception("Layer " + layer + " does not exist")
