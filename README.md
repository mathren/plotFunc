# My python setup to plot and analyze MESA output

I use these mostly to analyze data produced with [MESA](http://mesa.sourceforge.net/).<br>
If you are interested in something more sofisticated, check out [mesaplot](https://github.com/rjfarmer/mesaplot)

# How to use

*Disclaimer* This should _not_ be considered an example of the way
things are supposed to be done. Quite the contrary, in case of doubt.

Import the files that you are interested in using.
```  import sys
sys.path.append('/mnt/home/mrenzo/codes/python_stuff/mylib/')
from MESAreader import *
import matplotlib.pyplot as plt
from plotDefaults import *
