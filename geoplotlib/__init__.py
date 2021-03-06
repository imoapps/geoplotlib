import traceback
import pyglet
from geoplotlib.core import GeoplotlibApp


class AppConfig:

    def __init__(self):
        self.reset()


    def reset(self):
        self.layers = []
        self.bbox = None
        self.savefig = None
        self.tiles_provider = 'mapquest'
        self.smoothing = False
        self.map_alpha = 196
        screen =  pyglet.canvas.get_display().get_default_screen()
        self.screen_w = int(screen.width * .9)
        self.screen_h = int(screen.height * .9)


_global_config = AppConfig()


def _runapp(app_config):
    app = GeoplotlibApp(app_config)
    try:
        app.start()
    except:
        traceback.print_exc()
    finally:
        app.close()
        _global_config.reset()


def show():
    """Launch geoplotlib"""
    _runapp(_global_config)


def savefig(fname):
    """Launch geoplotlib, saves a screeshot and terminates"""
    _global_config.savefig = fname
    _runapp(_global_config)


def scatter(data, color=None, point_size=2, f_tooltip=None):
    """Create a scatterplot

    :param data: data access object
    :param color: color
    :param point_size: point size
    :param f_tooltip: function to return a tooltip string for a point
    """
    from geoplotlib.layers import ScatterLayer
    _global_config.layers.append(ScatterLayer(data, color=color, point_size=point_size, f_tooltip=f_tooltip))


def hist(data, cmap='hot', alpha=220, colorscale='sqrt', binsize=16, show_tooltip=False,
         scalemin=0, scalemax=None, f_group=None):
    """Create a 2D histogram

    :param data: data access object
    :param cmap: colormap name
    :param alpha: color alpha
    :param colorscale: scaling [lin, log, sqrt]
    :param binsize: size of the hist bins
    :param show_tooltip: if True, will show the value of bins on mouseover
    :param scalemin: min value for displaying a bin
    :param scalemax: max value for a bin
    :param f_group: function to apply to samples in the same bin. Default is to count
    :return:
    """
    from geoplotlib.layers import HistogramLayer
    _global_config.layers.append(HistogramLayer(data, cmap=cmap, alpha=alpha, colorscale=colorscale,
                                    binsize=binsize, show_tooltip=show_tooltip, scalemin=scalemin, 
                                    scalemax=scalemax, f_group=f_group))


def graph(data, src_lat, src_lon, dest_lat, dest_lon, linewidth=1, alpha=220, color='hot'):
    """Create a graph drawing a line between each pair of (src_lat, src_lon) and (dest_lat, dest_lon)

    :param data: data access object
    :param src_lat: field name of source latitude
    :param src_lon: field name of source longitude
    :param dest_lat: field name of destination latitude
    :param dest_lon: field name of destination longitude
    :param linewidth: line width
    :param alpha: color alpha
    :param color: color or colormap
    """
    from geoplotlib.layers import GraphLayer
    _global_config.layers.append(GraphLayer(data, src_lat, src_lon, dest_lat, dest_lon, linewidth, alpha, color))


def shapefiles(fname, f_tooltip=None, color=None, linewidth=3, shape_type='full'):
    """
    Load and draws shapefiles

    :param fname: full path to the shapefile
    :param f_tooltip: function to generate a tooltip on mouseover
    :param color: color
    :param linewidth: line width
    :param shape_type: either full or bbox
    """
    from geoplotlib.layers import ShapefileLayer
    _global_config.layers.append(ShapefileLayer(fname, f_tooltip, color, linewidth, shape_type))


def voronoi(data, line_color=None, line_width=2, f_tooltip=None, cmap=None, max_area=1e4, alpha=220):
    """
    Draw the voronoi tesselation of the points

    :param data: data access object
    :param line_color: line color
    :param line_width: line width
    :param f_tooltip: function to generate a tooltip on mouseover
    :param cmap: color map
    :param max_area: scaling constant to determine the color of the voronoi areas
    :param alpha: color alpha
    """
    from geoplotlib.layers import VoronoiLayer
    _global_config.layers.append(VoronoiLayer(data, line_color, line_width, f_tooltip, cmap, max_area, alpha))


def delaunay(data, line_color=None, line_width=2, cmap=None, max_lenght=100):
    """
    Draw a delaunay triangulation of the points

    :param data: data access object
    :param line_color: line color
    :param line_width: line width
    :param cmap: color map
    :param max_lenght: scaling constant for coloring the edges
    """
    from geoplotlib.layers import DelaunayLayer
    _global_config.layers.append(DelaunayLayer(data, line_color, line_width, cmap, max_lenght))


def convexhull(data, col, fill=True, point_size=4):
    """
    Convex hull for a set of points

    :param data: points
    :param col: color
    :param fill: whether to fill the convexhull polygon or not
    :param point_size: size of the points on the convexhull. Points are not rendered if None
    """
    from geoplotlib.layers import ConvexHullLayer
    _global_config.layers.append(ConvexHullLayer(data, col, fill, point_size))


def kde(data, bw, cmap='hot', method='hist', scaling='sqrt', alpha=220,
                 cut_below=None, clip_above=None, binsize=1, cmap_levels=10):
    """
    Kernel density estimation visualization

    :param data: data access object
    :param bw: kernel bandwidth (in screen coordinates)
    :param cmap: colormap
    :param method: if kde use KDEMultivariate from statsmodel, which provides a more accurate but much slower estimation.
        If hist, estimates density applying gaussian smoothing on a 2D histogram, which is much faster but less accurate
    :param scaling: colorscale, lin log or sqrt
    :param alpha: color alpha
    :param cut_below: densities below cut_below are not drawn
    :param clip_above: defines the max value for the colorscale
    :param binsize: size of the bins for hist estimator
    :param cmap_levels: discretize colors into cmap_levels levels
    """
    from geoplotlib.layers import KDELayer
    _global_config.layers.append(KDELayer(data, bw, cmap, method, scaling, alpha,
                 cut_below, clip_above, binsize, cmap_levels))


def markers(data, marker, f_tooltip=None, marker_preferred_size=32):
    """
    Draw markers

    :param data: data access object
    :param marker: full filename of the marker image
    :param f_tooltip: function to generate a tooltip on mouseover
    :param marker_preferred_size: size in pixel for the marker images
    """
    from geoplotlib.layers import MarkersLayer
    _global_config.layers.append(MarkersLayer(data, marker, f_tooltip, marker_preferred_size))


def clear():
    """
    Remove all existing layers
    """
    _global_config.layers = []


def tiles_provider(tiles_provider):
    """
    Set the tile provider

    :param tiles_provider: either one of the built-in providers
    ['watercolor', 'toner', 'toner-lite', 'mapquest', 'darkmatter','positron']
    or a custom provider in the form
    {'url': lambda zoom, xtile, ytile: 'someurl' % (zoom, xtile, ytile),
    'tiles_dir': 'mytiles',
    'attribution': 'my attribution'
    })
    """
    _global_config.tiles_provider = tiles_provider


def add_layer(layer):
    """
    Add a layer

    :param layer: a BaseLayer object
    """
    _global_config.layers.append(layer)


def set_bbox(bbox):
    """
    Set the map bounding box

    :param bbox: a BoundingBox object
    """
    _global_config.bbox = bbox


def set_smoothing(smoothing):
    """
    Enables OpenGL lines smoothing (antialiasing)

    :param smoothing: smoothing enabled or disabled
    """
    _global_config.smoothing = smoothing


def set_map_alpha(alpha):
    """
    Alpha color of the map tiles

    :param alpha: int between 0 and 255. 0 is completely dark, 255 is full brightness
    """
    if alpha < 0 or alpha > 255:
        raise Exception('invalid alpha '  + str(alpha))
    _global_config.map_alpha = alpha


def set_window_size(w, h):
    """
    Set the geoplotlib window size
    
    :param w: window width
    :param h: window height
    :return:
    """
    _global_config.screen_w = w
    _global_config.screen_h = h
