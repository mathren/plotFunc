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

from matplotlib import rc
from matplotlib import rcParams

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
rc('xtick.major', width=3, size=12, pad=5)
rc('ytick.major', width=3, size=12, pad=5)
rc('xtick.minor', width=3, size=6, visible=True)
rc('ytick.minor', width=3, size=6, visible=True)
# figsize
rc('figure', figsize=(10.,10.))
rc('image', cmap="viridis")

rcParams['text.latex.preamble'] = [r"\usepackage{color}"]
rcParams['text.latex.preamble'] = [r"\usepackage{xcolor}"]
rcParams['text.latex.preamble'] = [r"\usepackage{amsmath}"]



