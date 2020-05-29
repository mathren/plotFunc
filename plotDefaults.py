## author: Mathieu Renzo

## Author: Mathieu Renzo <mathren90@gmail.com>
## Keywords: files

## Copyright (C) 2019-2020 Mathieu Renzo

## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or (at
## your option) any later version.
##
## This program is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see http://www.gnu.org/licenses/.
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import rcParams
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, FuncFormatter, MaxNLocator
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatch
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

rc('text', usetex=True)
rc('font', serif='palatino')
# rc('font', weight='bolder')
rc('mathtext', default='sf')
rc("lines", markeredgewidth=2)
rc("lines", linewidth=3)
rc('axes', labelsize=30)  # 24
rc("axes", linewidth=2)  # 2)
# set fontsize
rc('xtick', labelsize=30)
rc('ytick', labelsize=30)
rc('legend', fontsize=30)  # 16
# ticks stuff
rc('xtick', top=True, direction='in')
rc('ytick', right=True, direction='in')
rc('xtick', direction='in')
rc('ytick', direction='in')
rc('xtick.major', width=2, size=12, pad=5)
rc('ytick.major', width=2, size=12, pad=5)
rc('xtick.minor', width=2, size=6, visible=True)
rc('ytick.minor', width=2, size=6, visible=True)
# colors
rc('figure', figsize=(10.,10.), facecolor="white", edgecolor="white", autolayout=True, frameon=False)
rc('axes', facecolor="white", linewidth=2)
rc('savefig', facecolor="white")
rc('image', cmap="viridis")
# error bars
rc('errorbar', capsize=2)
# legend
rc('legend', frameon=False)

rcParams['text.latex.preamble'] = [r"\usepackage{color}"]
rcParams['text.latex.preamble'] = [r"\usepackage{xcolor}"]
rcParams['text.latex.preamble'] = [r"\usepackage{amsmath}"]



## define some colors ----------------------------------------------------------------------

Yellow = "#DDDD77"
Green = "#88CCAA"
Blue = "#77AADD"
