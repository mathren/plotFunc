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
sys.path.append('path/to/folder/plotFunc/')
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

If using an ipython notebook, this needs to be done in a different
cell than the one containing `from plotDefaults import *`. The more
appropriate way to do this would be to create a matplotlibrc file as
explained
[here](https://matplotlib.org/tutorials/introductory/customizing.html).

# How to use compare_inlists.py

While experimenting with MESA and developing setups, I find myself
rather often comparing inlists (for single and/or binary stars) with
each other. A simple diff is often not particularly informative
because of the comments, non-matching order of the entries, or missing
entries in one file that are present in the other file but have no
real effect because they are set to the defaults. For this reason,
I've written the script `compare_inlists.py` which can print a
line-by-line diff of two inlists, ignoring comments and empty lines,
and checking the defaults from the documentation when entries are
missing. It *assumes you use the same MESA version* for this last task.

This can be used inside of scripts or notebooks, or from command line.

```
python compare_inlists.py --help                                                                                                ✔  8  15:05:26 
Usage: compare_inlists.py [OPTIONS] INLIST1 INLIST2

Options:
  --pgstar TEXT    Show also diff of pgstar namelists.
  --mesa_dir TEXT  use customized location of $MESA_DIR. Will use environment
                   variable if empty and return an error if empty.
  --vb TEXT        Show also matching lines using green.
  --help           Show this message and exit.
```

It uses `termcolor` to print in red entries that differ between
two inlists, and, if invoked adding `--vb=True` (for verbose) from the command
line it will also print in green entries that are equal. If one entry
is in one inlist but not the other, but the inlist that contains it 
has the default value, it is considered as a "green" entry.

This has been tested with MESA version 12778, and works for inlists
for single stars and binaries (but will refuse to compare input for a
single star and for a binary with each other). It can take a
customized `$MESA_DIR` with the optional argument `--mesa_dir`. If not
provided it will use the `$MESA_DIR` environment variable currently
set.

By default the comparison between pgstar namelist is disabled because
I need it less, but it can be enabled using `--pgstar=True`.



