from matplotlib.transforms import Bbox
from matplotlib.transforms import TransformedBbox
from matplotlib.transforms import blended_transform_factory
from mpl_toolkits.axes_grid1.inset_locator import BboxPatch
from mpl_toolkits.axes_grid1.inset_locator import BboxConnector
from mpl_toolkits.axes_grid1.inset_locator import BboxConnectorPatch
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np


class CrossLink(object):

    """ . """

    def __init__(
            self,
            ax1,
            ax2,
            ax1_yrange=(0, 1),
            ax2_yrange=(0, 1),
            add_to_axes=True,
            **kwargs
            ):
        """
        Keyword Arguments:
        ax1 -- The upper matplotlib axes instance.
        ax2 -- The lower matplotlib axes instance.
        ax1_yrange -- tuple as (ymin, ymax) where ymin \
            and ymax are between [0, 1]. default = (0, 1).
        ax2_yrange -- tuple as (ymin, ymax) where ymin \
            and ymax are between [0, 1]. default = (0, 1).
        add_to_axes -- add the patches to the axes (default = True).

        See <http://matplotlib.org/api/patches_api.html#matplotlib.patches.Patch>
        for valid kwargs.
        """
        self.ax1 = ax1
        self.ax2 = ax2
        self.ax1_yrange = ax1_yrange
        self.ax2_yrange = ax2_yrange

        self.transform_ax1 = blended_transform_factory(
            ax1.transData,
            ax1.transAxes
            )
        self.transform_ax2 = blended_transform_factory(
            ax2.transData,
            ax2.transAxes
            )
        self.add_to_axes = add_to_axes

        self.valid_kwargs = {
            "alpha", "animated", "antialiased",
            "axes", "capstyle", "clip_box",
            "clip_on", "clip_path", "color",
            "contains", "edgecolor", "facecolor",
            "figure", "fill", "gid", "hatch",
            "joinstyle", "label", "linestyle",
            "linewidth", "lod", "path_effects",
            "picker", "rasterized", "sketch_params",
            "snap", "transform", "url",
            "visible", "zorder", "ec", "fc",
            }
        self.properties = dict()
        self.properties['clip_on'] = False
        for key, value in kwargs.items():
            if key in self.valid_kwargs:
                self.properties[key] = value
        return

    def __call__(
            self,
            x1_start,
            x1_length,
            x2_start,
            x2_length,
            **kwargs
            ):
        """
        """
        properties = self.properties.copy()
        properties.update(kwargs)

        line_properties = {
            'clip_on': properties['clip_on'],
            'fill': False,
            'alpha': properties['alpha']
            }
        for prop in ['ec', 'edgecolor', 'lw',
                     'linewidth', "linestyle", "capstyle"]:
            if prop in properties:
                line_properties[prop] = properties.pop(prop)

        path, codes = self._draw_link(
            x1_start,
            x1_length,
            x2_start,
            x2_length,
            )

        link_patch = patches.PathPatch(
            Path(path, codes),
            transform=self.transform_ax1,
            linewidth=0.,
            **properties
            )
        link_patch_edges = patches.PathPatch(
            Path(path[:-1], codes[:-1]),
            transform=self.transform_ax1,
            **line_properties
            )

        path, codes = self._draw_ax2_box(
            x2_start,
            x2_length,
            )
        ax2_box_patch = patches.PathPatch(
            Path(path, codes),
            transform=self.transform_ax2,
            linewidth=0.,
            **properties
            )
        ax2_box_patch_edges = patches.PathPatch(
            Path(path[:-1], codes[:-1]),
            transform=self.transform_ax2,
            **line_properties
            )

        if self.add_to_axes:
            self.ax1.add_patch(link_patch)
            self.ax2.add_patch(ax2_box_patch)
            self.ax1.add_patch(link_patch_edges)
            self.ax2.add_patch(ax2_box_patch_edges)

        return link_patch, ax2_box_patch

    def _draw_link(
            self,
            x1_start,
            x1_length,
            x2_start,
            x2_length,
            ):
        """ . """

        codes = np.array([
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ])
        y1 = self.ax1_yrange
        y2 = self.ax2_yrange
        path = np.array([
            self.transform_ax2.transform([x2_start, y2[1]]),
            self.transform_ax1.transform([x1_start, y1[0]]),
            self.transform_ax1.transform([x1_start, y1[1]]),
            self.transform_ax1.transform([x1_start + x1_length, y1[1]]),
            self.transform_ax1.transform([x1_start + x1_length, y1[0]]),
            self.transform_ax2.transform([x2_start + x2_length, y2[1]]),
            self.transform_ax2.transform([x2_start, y2[1]]),
            ])
        path = np.apply_along_axis(self.transform_ax1.inverted().transform, 1, path)

        return path, codes

    def _draw_ax2_box(
            self,
            x2_start,
            x2_length,
            ):
        """ . """

        codes = np.array([
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ])
        y2 = self.ax2_yrange
        path = np.array([
            self.transform_ax2.transform([x2_start + x2_length, y2[1]]),
            self.transform_ax2.transform([x2_start + x2_length, y2[0]]),
            self.transform_ax2.transform([x2_start, y2[0]]),
            self.transform_ax2.transform([x2_start, y2[1]]),
            self.transform_ax2.transform([x2_start + x2_length, y2[1]]),
            ])
        path = np.apply_along_axis(self.transform_ax2.inverted().transform, 1, path)

        return path, codes

class SelfLink(object):

    """ . """

    def __init__(self,
            ax,
            yrange=(0, 1),
            add_to_axes=True,
            y_scaling=2,
            **kwargs
            ):
        """
        Keyword Arguments:
        ax -- The upper matplotlib axes instance.
        yrange -- tuple as (ymin, ymax) where ymin \
            and ymax are between [0, 1]. default = (0, 1).
        add_to_axes -- add the patches to the axes (default = True).

        See <http://matplotlib.org/api/patches_api.html#matplotlib.patches.Patch>
        for valid kwargs.
        """
        self.ax = ax
        self.yrange = yrange
        self.transform_ax = blended_transform_factory(
            ax.transData,
            ax.transAxes
            )
        self.add_to_axes = add_to_axes
        self.y_scaling = y_scaling

        self.valid_kwargs = {
            "alpha", "animated", "antialiased",
            "axes", "capstyle", "clip_box",
            "clip_on", "clip_path", "color",
            "contains", "edgecolor", "facecolor",
            "figure", "fill", "gid", "hatch",
            "joinstyle", "label", "linestyle",
            "linewidth", "lod", "path_effects",
            "picker", "rasterized", "sketch_params",
            "snap", "transform", "url",
            "visible", "zorder", "ec", "fc",
            }
        self.properties = dict()
        self.properties['clip_on'] = False
        for key, value in kwargs.items():
            if key in self.valid_kwargs:
                self.properties[key] = value
        return

    def __call__(
            self,
            x1_start,
            x1_length,
            x2_start,
            x2_length,
            y_scaling=None,
            **kwargs
            ):
        """ . """
        properties = self.properties.copy()
        properties.update(kwargs)
        if y_scaling is None:
            y_scaling = self.y_scaling

        path, codes = self._draw(
            x1_start,
            x1_length,
            x2_start,
            x2_length,
            y_scaling=y_scaling
            )
        link_patch = patches.PathPatch(
            Path(path, codes),
            transform=self.transform_ax,
            **properties
            )

        if self.add_to_axes:
            self.ax.add_patch(link_patch)

        return link_patch

    def _draw(
            self,
            x1_start,
            x1_length,
            x2_start,
            x2_length,
            y_scaling=2
            ):
        """ . """

        length_a = abs(x1_start - (x2_start + x2_length))
        display_coords_a = self.ax.transData.transform([length_a, 0])
        width_a = y_scaling * self.ax.transAxes.inverted().transform(display_coords_a)[0]

        length_b = abs((x1_start + x1_length) - x2_start)
        display_coords_b = self.ax.transData.transform([length_b, 0])
        width_b = y_scaling * self.ax.transAxes.inverted().transform(display_coords_b)[0]


        codes = np.array([
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY
            ])

        y = self.yrange
        path = np.array([
            [x1_start, y[1]],
            [x1_start, y[1] + width_a],
            [x2_start + x2_length, y[1] + width_a],
            [x2_start + x2_length, y[1]],
            [x2_start + x2_length, y[0]],
            [x2_start, y[0]],
            [x2_start, y[1]],
            [x2_start, y[1] + width_b],
            [x1_start + x1_length, y[1] + width_b],
            [x1_start + x1_length, y[1]],
            [x1_start + x1_length, y[0]],
            [x1_start, y[0]],
            [x1_start, y[1]],
            [x1_start, y[0]],
            ])

        return path, codes
