# author: Mathieu Renzo

# Author: Mathieu Renzo <mathren90@gmail.com>
# Keywords: files

# Copyright (C) 2019-2022 Mathieu Renzo

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import rcParams
# from matplotlib.ticker import MultipleLocator, FormatStrFormatter, FuncFormatter, MaxNLocator
import matplotlib.gridspec as gridspec
# import matplotlib.patches as mpatch
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

def set_plot_defaults_from_matplotlibrc(root="../src/figures/"):
    """
    given the path of the folder containing the matplotlibrc parses
    the matplotlibrc and set the non-commented parameters.  By default
    it assumes the folder where matplotlibrc is to be ../src/data for
    a showyourwork workflow where notebooks are outside of src.

    Parameters:
    ----------
    root: `string` absolute path to the folder containing the matplotlibrc file to read.
    """
    # for some reason if you run this function in the same cell containing
    #          ``` from plotDefaults import * ```
    # it will not work as intended. Run it in a separate cell and it works.
    # TODO: understand and fix this behavior.
    from matplotlib import rcParams
    with open(root+"/matplotlibrc", "r") as f:
        for i, line in enumerate(f):
            L = line.rstrip().lstrip()
            if not L: continue # skip empty lines
            if L[0] != "#": # skip commented lines
                # read the line
                uncommented_line = L.split("#")[0].rstrip().lstrip()
                group_param = uncommented_line.split(":")[0].rstrip().lstrip()
                val = uncommented_line.split(":")[-1].rstrip().lstrip()
                # fix figsize
                if "figsize" in group_param:
                    length = tuple(val.split(','))
                rcParams[group_param] = val
    print("done reading matplotlibrc")

def set_plot_defaults():
    """ old way of setting up defaults, maintained for legacy """
    try:
        set_plot_defaults_from_matplotlibrc(".")
        return
    except:
        print("No local matplotlibrc")
        # sets rc param that I like
        # these are also in ./matplotlibrc
        # for some reason if you run this function in the same cell containing
        #          ``` from plotDefaults import * ```
        # it will not work as intended. Run it in a separate cell and it works
        # TODO: understand and fix this behavior.
        rc("text", usetex=True)
        rc("font", serif="palatino")
        rc("font", weight="bold")
        rc("mathtext", default="sf")
        rc("lines", markeredgewidth=2)
        rc("lines", linewidth=3)
        rc("axes", labelsize=30)
        rc("axes", linewidth=2)
        # set fontsize
        rc("xtick", labelsize=30)
        rc("ytick", labelsize=30)
        rc("legend", fontsize=30)
        # ticks stuff
        rc("xtick", top=True, direction="in")
        rc("ytick", right=True, direction="in")
        rc("xtick.major", width=2, size=12, pad=12)
        rc("ytick.major", width=2, size=12, pad=12)
        rc("xtick.minor", width=2, size=6, visible=True)
        rc("ytick.minor", width=2, size=6, visible=True)
        rc(
            "figure",
            figsize=(8.0, 8.0),
            facecolor="white",
            edgecolor="white",
            autolayout=True,
            frameon=False,
        )
        rc("axes", facecolor="white", linewidth=2)
        rc("savefig", facecolor="white", bbox="tight")
        rc("image", cmap="viridis")
        rc("errorbar", capsize=2)
        rc("legend", frameon=False)
        rc("legend", fontsize=30)
        print("done in plot_defaults.py")


# ---------------------------------------------------------------------
# auxiliary functions for plotting

def make2Dmap(x, y, z, x1=0, x2=1, y1=0, y2=1, res=20):
    minx = min(min(x),x1)
    maxx = min(max(x),x2)
    miny = min(min(y),y1)
    maxy = min(max(y),y2)

    x_int = np.linspace(minx,maxx,res)
    y_int = np.linspace(miny,maxy,res)

    mat = np.zeros([len(x_int),len(y_int)])
    for i in range(0,len(x_int)-1):
        for j in range(0,len(y_int)-1):
            mat[j,i] = np.sum(z[(x>=x_int[i])*(x<x_int[i+1])*(y>=y_int[j])*(y<y_int[j+1])])
    return x_int, y_int, mat


def writePreliminary(ax):
    """
    Parameters:
    ----------
    ax: `maplotlib.axes`
    """
    ax.text(0.5,0.5,r"{\bf PRELIMINARY}", color="#808080",
            alpha=0.4, fontsize=74,ha='center', va='center', rotation=45, transform=ax.transAxes)


def my_mark_inset(parent_axes, inset_axes, loc1a=1, loc1b=1, loc2a=2, loc2b=2, **kwargs):
    from mpl_toolkits.axes_grid1.inset_locator import TransformedBbox, BboxPatch, BboxConnector
    rect = TransformedBbox(inset_axes.viewLim, parent_axes.transData)

    pp = BboxPatch(rect, fill=False, **kwargs)
    parent_axes.add_patch(pp)

    p1 = BboxConnector(inset_axes.bbox, rect, loc1=loc1a, loc2=loc1b, **kwargs)
    inset_axes.add_patch(p1)
    p1.set_clip_on(False)
    p2 = BboxConnector(inset_axes.bbox, rect, loc1=loc2a, loc2=loc2b, **kwargs)
    inset_axes.add_patch(p2)
    p2.set_clip_on(False)

    return pp, p1, p2
