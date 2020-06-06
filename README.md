# My python setup to plot and analyze MESA output

I use these mostly to analyze data produced with [MESA](http://mesa.sourceforge.net/).<br>
If you are interested in something more sofisticated, check out [mesaplot](https://github.com/rjfarmer/mesaplot)

# How to use

***Disclaimer*** This should _not_ be considered an example of the way
things are supposed to be done. Quite the contrary, in case of doubt.

Import the files that you are interested in using. I usually have these
files saved in a folder `path/to/folder` and use the sys module to add
this folder to path, like:

```
import sys
sys.path.append('path/to/folder/')
from MESAreader import *
from plotDefaults import *
from compare_inlists import *
```

To setup matplotlib the way I like it I define in `plotDefaults.py`
that can be called to set some rcParams:

```
>>> set_plotDefaults()
done in plotDefaults.py
```

The more appropriate way to do this would be to create a matplotlibrc
file as explained [here](https://matplotlib.org/tutorials/introductory/customizing.html).

# How to use compare_inlists.py

While experimenting with MESA and developing setups, I find myself
rather often comparing inlists (for single and/or binary stars) with
each other. A simple diff is often not particularyly informative because of the
comments, order of the entries, or missing entries in one file that
are present in the other file but anyways set to the defaults. For
this reason, I've written the script `compare_inlists.py` which can
print a line-by-line diff of two inlists, ignoring comments and empty
lines, and checking the defaults from the documentation when entries
are missing. It assumes you use the same MESA version for this last task.

It uses `termcolor` to print in red entries that differ between
two inlists, and, if invoked adding vb (for verbose) from the command
line it will also print in green entries that are equal. If one entry
is in one inlist but not the other, but the inlist that contains it 
has the default value, it is considered as a "green" entry.

This has been tested with MESA version 12778, and works for inlists
for single stars and binaries (but will refuse to compare input for a single
star and for a binary with each other). The functions it uses can also
take a MESA_DIR as optional argument, but for now from command line it
will use the `$MESA_DIR` environment variable.

To use it from your command line:

```
python compare_inlist.py /path/to/inlist1 /path/to/inlist2
```

or, if you also want to see entries that are equal

```
python compare_inlist.py /path/to/inlist1 /path/to/inlist2 vb
```

(actually right now any argument beyond the two inlists paths will be
interpreted as a wish for verbosity).
