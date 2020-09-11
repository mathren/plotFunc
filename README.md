# My python setup to plot and analyze MESA output

I use these mostly to analyze data produced with [MESA](http://mesa.sourceforge.net/).<br>
If you are interested in something more sofisticated, check out [mesaplot](https://github.com/rjfarmer/mesaplot).

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
```

Of course you can and should import only what you need and not
necessarily everything.

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
<!-- why? -->
