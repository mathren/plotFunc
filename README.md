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
python compare_inlists.py --help


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

## Example

```<pre><font color="#4D9A05">inlist_project                </font>	<font color="#4D9A05">save_model_when_terminate=.false.                                      </font>
<font color="#4D9A05">default                       </font>	<font color="#4D9A05">save_model_when_terminate=.false.                                      </font>

<font color="#CC0000">inlist_project                </font>	<font color="#CC0000">create_pre_main_sequence_model=.true.                                       </font>
<font color="#CC0000">inlist                        </font>	<font color="#CC0000">missing</font>
<font color="#CC0000">default                       </font>	<font color="#CC0000">create_pre_main_sequence_model=.false.                                      </font>

<font color="#CC0000">inlist_project                </font>	<font color="#CC0000">pgstar_flag=.true.                                       </font>
<font color="#CC0000">inlist                        </font>	<font color="#CC0000">missing</font>
<font color="#CC0000">default                       </font>	<font color="#CC0000">pgstar_flag=.false.                                      </font>

<font color="#CC0000">inlist_project                </font>	<font color="#CC0000">save_model_filename=&apos;15M_at_TAMS.mod&apos;                            </font>
<font color="#CC0000">inlist                        </font>	<font color="#CC0000">missing</font>
<font color="#CC0000">default                       </font>	<font color="#CC0000">save_model_filename=&apos;undefined&apos;                                  </font>

<font color="#CC0000">inlist                        </font>	<font color="#CC0000">mesa_dir=&apos;../../..&apos;                                   </font>
<font color="#CC0000">inlist_project                </font>	<font color="#CC0000">missing</font>
<font color="#CC0000">default                       </font>	<font color="#CC0000">mesa_dir=&apos;&apos;                                           </font>

<font color="#CC0000">inlist                        </font>	<font color="#CC0000">read_extra_star_job_inlist2=.true.                                       </font>
<font color="#CC0000">inlist_project                </font>	<font color="#CC0000">missing</font>
<font color="#CC0000">default                       </font>	<font color="#CC0000">read_extra_star_job_inlist2=.false.                                      </font>

<font color="#CC0000">inlist                        </font>	<font color="#CC0000">extra_star_job_inlist2_name=&apos;inlist_15M_dynamo&apos;                          </font>
<font color="#CC0000">inlist_project                </font>	<font color="#CC0000">missing</font>
<font color="#CC0000">default                       </font>	<font color="#CC0000">extra_star_job_inlist2_name=&apos;undefined&apos;                                  </font>

------end job namelist------
<font color="#CC0000">inlist_project                </font>	<font color="#CC0000">use_dedt_form_of_energy_eqn=.true.                                       </font>
<font color="#CC0000">inlist                        </font>	<font color="#CC0000">missing</font>
<font color="#CC0000">default                       </font>	<font color="#CC0000">use_dedt_form_of_energy_eqn=.false.                                      </font>

<font color="#4D9A05">inlist_project                </font>	<font color="#4D9A05">use_gold_tolerances=.true.                                       </font>
<font color="#4D9A05">default                       </font>	<font color="#4D9A05">use_gold_tolerances=.true.                                       </font>

<font color="#CC0000">inlist_project                </font>	<font color="#CC0000">xa_central_lower_limit(1)=0.001                                        </font>
<font color="#CC0000">inlist                        </font>	<font color="#CC0000">missing</font>
<font color="#CC0000">default                       </font>	<font color="#CC0000">xa_central_lower_limit(1)=0.0                                          </font>

<font color="#CC0000">inlist_project                </font>	<font color="#CC0000">xa_central_lower_limit_species(1)=&apos;h1&apos;                                         </font>
<font color="#CC0000">inlist                        </font>	<font color="#CC0000">missing</font>
<font color="#CC0000">default                       </font>	<font color="#CC0000">xa_central_lower_limit_species(1)=&apos;&apos;                                           </font>

<font color="#CC0000">inlist_project                </font>	<font color="#CC0000">stop_near_zams=.true.                                       </font>
<font color="#CC0000">inlist                        </font>	<font color="#CC0000">missing</font>
<font color="#CC0000">default                       </font>	<font color="#CC0000">stop_near_zams=.false.                                      </font>

<font color="#CC0000">inlist_project                </font>	<font color="#CC0000">lnuc_div_l_zams_limit=0.99                                         </font>
<font color="#CC0000">inlist                        </font>	<font color="#CC0000">missing</font>
<font color="#CC0000">default                       </font>	<font color="#CC0000">lnuc_div_l_zams_limit=0.9                                          </font>

<font color="#CC0000">inlist_project                </font>	<font color="#CC0000">initial_mass=15.0                                         </font>
<font color="#CC0000">inlist                        </font>	<font color="#CC0000">missing</font>
<font color="#CC0000">default                       </font>	<font color="#CC0000">initial_mass=1.0                                          </font>

<font color="#CC0000">inlist                        </font>	<font color="#CC0000">extra_controls_inlist1_name=&apos;inlist_15M_dynamo&apos;                          </font>
<font color="#CC0000">inlist_project                </font>	<font color="#CC0000">missing</font>
<font color="#CC0000">default                       </font>	<font color="#CC0000">extra_controls_inlist1_name=&apos;undefined&apos;                                  </font>

<font color="#CC0000">inlist                        </font>	<font color="#CC0000">read_extra_controls_inlist1=.true.                                       </font>
<font color="#CC0000">inlist_project                </font>	<font color="#CC0000">missing</font>
<font color="#CC0000">default                       </font>	<font color="#CC0000">read_extra_controls_inlist1=.false.                                      </font>

------end controls namelist------
done!
</pre>

```

```
inlist_project                	save_model_when_terminate=.false.                                      
default                       	save_model_when_terminate=.false.                                      

inlist_project                	create_pre_main_sequence_model=.true.                                       
inlist                        	missing
default                       	create_pre_main_sequence_model=.false.                                      

inlist_project                	pgstar_flag=.true.                                       
inlist                        	missing
default                       	pgstar_flag=.false.                                      

inlist_project                	save_model_filename='15M_at_TAMS.mod'                            
inlist                        	missing
default                       	save_model_filename='undefined'                                  

inlist                        	mesa_dir='../../..'                                   
inlist_project                	missing
default                       	mesa_dir=''                                           

inlist                        	read_extra_star_job_inlist2=.true.                                       
inlist_project                	missing
default                       	read_extra_star_job_inlist2=.false.                                      

inlist                        	extra_star_job_inlist2_name='inlist_15M_dynamo'                          
inlist_project                	missing
default                       	extra_star_job_inlist2_name='undefined'                                  

------end job namelist------
inlist_project                	use_dedt_form_of_energy_eqn=.true.                                       
inlist                        	missing
default                       	use_dedt_form_of_energy_eqn=.false.                                      

inlist_project                	use_gold_tolerances=.true.                                       
default                       	use_gold_tolerances=.true.                                       

inlist_project                	xa_central_lower_limit(1)=0.001                                        
inlist                        	missing
default                       	xa_central_lower_limit(1)=0.0                                          

inlist_project                	xa_central_lower_limit_species(1)='h1'                                         
inlist                        	missing
default                       	xa_central_lower_limit_species(1)=''                                           

inlist_project                	stop_near_zams=.true.                                       
inlist                        	missing
default                       	stop_near_zams=.false.                                      

inlist_project                	lnuc_div_l_zams_limit=0.99                                         
inlist                        	missing
default                       	lnuc_div_l_zams_limit=0.9                                          

inlist_project                	initial_mass=15.0                                         
inlist                        	missing
default                       	initial_mass=1.0                                          

inlist                        	extra_controls_inlist1_name='inlist_15M_dynamo'                          
inlist_project                	missing
default                       	extra_controls_inlist1_name='undefined'                                  

inlist                        	read_extra_controls_inlist1=.true.                                       
inlist_project                	missing
default                       	read_extra_controls_inlist1=.false.                                      

------end controls namelist------
done!

``
