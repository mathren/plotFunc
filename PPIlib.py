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

# import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
import sys
import glob
import time
import math
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, FuncFormatter, MaxNLocator
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatch
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from termcolor import colored
# parallelization stuff
from joblib import Parallel, delayed
import multiprocessing
from utilsLib import tail
from MESAreader import getSrcCol
## define some colors ----------------------------------------------------------------------

Yellow = "#DDDD77"
Green = "#88CCAA"
Blue = "#77AADD"

## constants -------------------------------------------------------------------------------
global secyer
secyer = 3.1558149984e7
global Lsun
Lsun = 3.8418e33
global Msun
Msun = 1.9892e33
global Rsun_cm
Rsun_cm = 6.9598e10 # in cm
global G_cgs
G_cgs = 6.67428e-8 # in cgs


## File management -------------------------------------------------------------------------
def getEjectaFile(f):
    fname = f+'ejecta.data'
    F = open(fname, 'r')
    for i, line in enumerate(F):
        if i==0:
            col = line.split()
            break
    src = reader(fname, len(col),1)
    F.close()
    return src, col

def getHistoryFile(f):
    if os.path.isfile(f+'LOGS/history.data'):
        hfile = f+'LOGS/history.data'
    elif os.path.isfile(f+'/history.data'):
        hfile = f+'/history.data'
    else:
        print(colored("CAN'T FIND HISTORY FILE!","red"))
        hfile = ''
    return hfile


def getFinalProfile(f):
    # Pablo's setup
    if os.path.isfile(f+'/LOGS/pisn_prof.data'):
        return f+'/LOGS/pisn_prof.data'
    elif os.path.isfile(f+'/pisn_prof.data'):
        return f+'/pisn_prof.data'
    elif len(glob.glob(f+'/LOGS/*final_prof*'))==1:
        return glob.glob(f+'/LOGS/*final_prof*')[0]
    elif len(glob.glob(f+'/LOGS1/*final_prof*'))==1:
        return glob.glob(f+'/LOGS1/*final_prof*')[0]
    elif len(glob.glob(f+'/LOGS2/*final_prof*'))==1:
        return glob.glob(f+'/LOGS2/*final_prof*')[0]
    elif len(glob.glob(f+'/*final_prof.data'))==1:
        return glob.glob(f+'/*final_prof.data')[0]
    elif 'RUNSTAR3' in f:
        # # my setup
        if os.path.isfile(f+'/LOGS/profiles.index'):
            F = open(f+'/LOGS/profiles.index')
            L = F.readlines()
            ll = L[-1]
            num = ll.split()[-1]
            return f+'/LOGS/profile'+str(num)+'.data'
        elif len(glob.glob(f+'/profile*.data'))==1:
            return glob.glob(f+'/profile*.data')[0]
    else:
        print(colored("cannot find final profile!","red"))
        return ''


def getPrePulseProfile(f):
    if len(glob.glob(f+'/pre-pulse.data'))==1:
        return glob.glob(f+'/pre-pulse.data')[0]
    elif len(glob.glob(f+'/preSN.data'))==1:
        return glob.glob(f+'/pre-SN.data')[0]
    else:
        print(colored("cannot find pre-pulse profile!","red"))
        return ''


### Plotting --------------------------------------------------------------------------------------------------------------------

# EOS pulse onset
## this one instead comes from instability_EOS.ipynb
def plot_instability_region(ax,c='#f4e109', lw=2, ls='--',zorder=1):
    folder='/mnt/home/mrenzo/codes/mesa/mesa_11123/mesa11123/data/star_data/plot_info/'
    f = np.genfromtxt(folder+'gamma_4_thirds.data')
    xx = f[:, 0] # log10 density
    yy = f[:, 1] # log10 temperature
    #ax.plot(xx,yy,lw=3, ls='--',color=c)
    #ax.scatter(xx,yy)
    ax.plot(xx,yy,ls=ls,c=c,lw=lw, zorder=zorder)
    ax.fill_between(xx,yy, color=c, alpha=0.5, zorder=0)
    ax.set_xlim(2,6.25)
    ax.set_ylim(8.5, 10)



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



## Pulses -------------------------------------------------------------------------------------
def getModNumRelax(f):
    modnum_relax = []
    ## where are relaxations
    for fpulse in glob.glob(f+'/prerelax*'):
        F = open(fpulse,"r")
        for i, line in enumerate(F):
            if i == 1:
                hc = line.split()
                # print hc
            if i == 2:
                d = np.array(line.split())
                # print d
                break
        F.close()
        modnum_relax.append(int(d[hc.index("model_number")]))
    return modnum_relax

def SplitArray(a,krelax):
    ## given a list krelax of indexes
    ## returns list og slices of a that stop at the elements of krelax
    krelax=[0]+krelax+[len(a)] # add extrema
    # print krelax
    list = []
    for i in range(0,len(krelax)-1):
        list.append(a[krelax[i]:krelax[i+1]])
    return list # length = input krelax+1


def Notupperlimit(f):
    # returns True if the folder f contains an upperlimit model pulsating while collapsing
    # returns False otherwise
    # So has to be used like if(Notupperlimit(f)): do things for normal model else: do things for upperlimits
    if 'RUNSTAR3' in f:
        list = ['33.5,47.5']
        for l in list:
            if l in f: return False #it's un upperlimits
    # else:
    #     print colored("no-upperlimits check","yellow")
    return True

def findPulses_mejection(f,show_plot=False):
    # speed up, will not work at first try
    if (show_plot == False):
        fname = f+'/PLOTS/pulse_info.data'
        if (os.path.isfile(fname)):
        # don't want to see plot and file already exists?
        ## then it can either be CC of PPI+CC
            F = open(fname,'r')
            for i, line in enumerate(F):
                if i == 0 :
                    header = line.split()
                    break
            src = reader(fname, len(header),1)
            if len(src) == 0:
                pulses = "CC"
                cnt = 0
                return pulses, cnt
            if len(np.shape(src))==1 and len(src)>1:
                cnt = 1
                pulses = "PPI+CC"
                return pulses, cnt
            elif len(np.shape(src))>1:
                cnt = len(src[:,1])
                pulses = "PPI+CC"
                return pulses, cnt
        else: #PISN or CC?
            pulses = "CC"
            cnt = 0
            ## read outputfile
            outputfile = f+'/output'
            end_out = tail(outputfile,50)
            # print end_out
            for i in range(len(end_out)-1,0,-1):
                line = str(end_out[i])
                # print line
                if (('terminated evolution: cannot find acceptable model' in line) or
                    ('termination code: min_timestep_limit' in line) or
                    ('stopping because of problems -- too many retries' in line) or
                    ('stop because model_number >= max_model_number' in line)):
                    pulses = "failed"
                    return pulses, np.nan
                elif (('star is going PISN!' in line) or ('above the escape velocity, PISN!' in line)):
                    pulses = "PISN"
                    return pulses, 1
            return pulses , cnt
    else:
        # initialize
        pulses = 'CC'
        cnt = 0
        if 'RUNSTAR3' in f:
            # ad hoc fix for old grid
            print(colored("old grid", "blue"))
            if os.path.isfile(f+'/pulse001.data'):
                pulses = "PPI+CC"
                cnt = len(glob.glob(f+'/pulse*.data'))
            ## check for PISN
            outputfile = f+'/output'
            end_out = tail(outputfile,50)
            # print end_out
            for i in range(len(end_out)-1,0,-1):
                line = end_out[i]
                # print line
                if (('terminated evolution: cannot find acceptable model' in line) or
                    ('termination code: min_timestep_limit' in line) or
                    ('stopping because of problems -- too many retries' in line) or
                    ('stop because model_number >= max_model_number' in line)):
                    pulses = "failed"
                elif (('star is going PISN!' in line) or ('above the escape velocity, PISN!' in line)):
                    pulses = "PISN"
            if (pulses == "PISN"):
                return pulses, 1
            elif (pulses == "failed"):
                return pulses, np.nan
        elif ("RUNSTAR3" not in f): ## check for number of pulses
            outputfile = f+'/output'
            end_out = tail(outputfile,50)
            # print end_out
            for i in range(len(end_out)-1,0,-1):
                line = end_out[i]
                # print line
                if (('terminated evolution: cannot find acceptable model' in line) or
                    ('termination code: min_timestep_limit' in line) or
                    ('stopping because of problems -- too many retries' in line) or
                    ('stop because model_number >= max_model_number' in line)):
                    pulses = "failed"
                    return pulses, np.nan
                elif (('star is going PISN!' in line) or ('above the escape velocity, PISN!' in line)):
                    pulses = "PISN"
                    return pulses, 1
            ## it's not PISN, CC or failed, count the pulses
            # get overall data
            src, col = getEjectaFile(f)
            modnum = src[:,col.index("model_number")]
            t_cc = src[-1, col.index("star_age")]*secyer
            t_all  = src[:, col.index("star_age")]*secyer
            m_ej = src[:,col.index("dm")] #
            v_ej = src[:, col.index("v_cm")]
            ## get tdyn for bound stuff
            hsrc, hcol = getSrcCol(getHistoryFile(f))
            m_bound = hsrc[:, hcol.index("M_below_vesc")]*Msun # g
            R = 10**(hsrc[:, hcol.index("photosphere_log_r")])*Rsun_cm
            t_dyn = 2*math.pi*np.sqrt(R**3/(G_cgs*m_bound)) # sec
            # make plot for pulsating models
            fig = plt.figure(figsize=(20., 10.))
            gs = gridspec.GridSpec(100, 100)
            ax = fig.add_subplot(gs[:,:50])
            bx = fig.add_subplot(gs[:,50:])
            # make plot
            ind = m_ej != 0
            x = np.log10((t_cc-t_all)/secyer)
            ax.scatter(modnum[ind],m_ej[ind],s=150,c='b',edgecolor="b",zorder=0)
            bx.scatter(x[ind],np.cumsum(m_ej)[ind],s=150,c='b',edgecolor="b",zorder=0)
            # get number of relaxations
            krelax = getModNumRelax(f)
            for k in range(0, len(krelax)):
                bx.axvline(np.log10((t_cc-t_all[krelax[k]])/secyer),0,1,lw=2, color="k", ls="--")
                ax.axvline(krelax[k],0,1,lw=2, color="k", ls="--")
            # # prepare summary file
            pinfo_file = open(f+'/PLOTS/pulse_info.data','w')
            header = "pulse_num\t\tdm_pulse\t\tt_start\t\tt_end\t\tduration_div_tdyn_start\t\tavg_v_pulse\t\ttimestep_start\t\ttimestep_end\n"
            pinfo_file.writelines(header)
            ## count jumps in cumulative with DM > mthreshold and DT>tdyn
            cnt = 0
            cum_m_ej = np.cumsum(m_ej)#
            ##############################
            mthreshold = 1e-6 #1e-5 # Msun
            ##############################
            ### for each part in between relaxations
            list_cum_m_ej = SplitArray(cum_m_ej, krelax)
            list_t_all = SplitArray(t_all, krelax)
            list_tdyn = SplitArray(t_dyn, krelax)
            list_modnum = SplitArray(modnum, krelax)
            list_m_ej = SplitArray(m_ej, krelax)
            list_tdyn = SplitArray(t_dyn,krelax)
            list_v_ej = SplitArray(v_ej, krelax)
            # track amount of mass lost across remesh
            m_already_ejected = 0

            for K in range(len(list_cum_m_ej)):
                # print "dealing with chunk", K
                cum_m_ej_aux = list_cum_m_ej[K]
                t_all_aux    = list_t_all[K]
                tdyn_aux     = list_tdyn[K]
                modnum_aux   = list_modnum[K]
                m_ej_aux     = list_m_ej[K]
                t_dyn_aux    = list_tdyn[K]
                v_ej_aux     = list_v_ej[K]
                # initialize
                i = 0
                in_pulse_flag = False
                # loop until end of this chunk
                while i<len(cum_m_ej_aux):
                    if (not in_pulse_flag):
                        # look for beginning of a pulse
                        if ((m_ej_aux[i] > mthreshold) or  # enough mass loss at this step or
                            (cum_m_ej_aux[i] - m_already_ejected >= mthreshold)): # since last pulse we have cumulated enough mass loss
                            # print "pulse start", i, cum_m_ej_aux[i] - m_already_ejected
                            in_pulse_flag = True
                            i_pulse_start = i
                            step_start = cum_m_ej_aux[i_pulse_start]
                            modnum_start = int(modnum_aux[i_pulse_start])
                            t_start = t_all_aux[i_pulse_start]
                            t_dyn_start = t_dyn_aux[i_pulse_start]
                            x_start = modnum_start #np.log10((t_cc-t_start)/secyer) #
                            y_start = m_ej_aux[i_pulse_start]
                            ax.scatter(x_start, y_start, marker='o',s=500, lw=0, color='g', alpha=0.5,zorder=1)
                            bx.scatter(np.log10((t_cc-t_start)/secyer),cum_m_ej_aux[i_pulse_start], marker='o',s=500, lw=0, color='g', alpha=0.5,zorder=1)
                            i += 1 # min pulse duration in timesteps, for speedup purposes
                        else:
                            i += 1
                    else: ## we are in a pulse
                        # check if enough mass is being lost from beginning of the pulse
                        if (cum_m_ej_aux[i]-step_start <= mthreshold): ## and
                            i+=1
                        else: # have enough mass loss
                            # check that at least a dynamical timescale has passed
                            if ((t_all_aux[i] - t_start) > t_dyn_start):
                                ## and remaining mass loss for 100 tdyn < current mass loss (=> flattening)
                                ## check that there is no significant mass loss in the next 100 dynamical timescale
                                tdyn_now = t_dyn_aux[i]
                                now = t_all_aux[i]
                                # get index of time now+tdyn_now
                                jmax = np.argmin(np.absolute(t_all_aux[:]-(now+100*tdyn_now)))
                                if jmax == i: ## reach the end of the array?
                                    control = 1e-99 ## pass test for free
                                else:
                                    control = np.cumsum(m_ej_aux[i:jmax])[-1]
                                # print control, i, jmax, "shit"
                                # check that in the next 100t_dyn from now we lose less than 0.1 mthreshold
                                if (control <= 0.1*mthreshold):
                                    # if here:
                                    # there is enough mass loss (DM>mthreshold)
                                    # enough time since beginning of pulse has elapsed (now - t_start > t_dyn_start)
                                    # we have reached the end of the array (before CC or remesh) or
                                    # the cumulative mass loss in the next 100 t_dyn is smaller than 1/10 mthreshold
                                    # this is defined as end of pulse
                                    in_pulse_flag = False
                                else: # too much mass loss in the future
                                    i+=1
                            else: # not enough time passed
                                i+=1
                            if i == len(cum_m_ej_aux)-1:
                                # end of loop
                                in_pulse_flag = False
                                if t_cc == t_all_aux[i]:
                                    i_pulse_end_aux = i-1
                        if (in_pulse_flag == False):
                            i_pulse_end = i
                            modnum_end = int(modnum_aux[i_pulse_end])
                            step_end = cum_m_ej_aux[i_pulse_end]
                            t_end = t_all_aux[i_pulse_end]
                            cnt += 1
                            ## get average CM velocity for entire pulse
                            avg_v = np.sum(v_ej_aux[i_pulse_start:i_pulse_end]*m_ej_aux[i_pulse_start:i_pulse_end])/(np.sum(m_ej_aux[i_pulse_start:i_pulse_end]))
                            # print avg_v
                            line = str(cnt)+"\t\t"+str(step_end-step_start)+"\t\t"+str(t_start)+"\t\t"+str(t_end)+"\t\t"+str((t_end-t_start)/t_dyn_start)+"\t\t"+str(avg_v)+"\t\t"+str(modnum_start)+"\t\t"+str(modnum_end)+"\n"
                            pinfo_file.writelines(line)
                            ## now plot
                            try:
                                i_pulse_end = min(i_pulse_end, i_pulse_end_aux)
                            except:
                                pass
                            x_end = modnum_end # np.log10((t_cc-t_all_aux[i_pulse_end])/secyer) # modnum_aux[i_pulse_end]#
                            y_end = m_ej_aux[i_pulse_end]
                            ax.scatter(x_end, y_end, marker='x',s=100, lw=2, color='r', zorder=2)
                            bx.scatter(np.log10((t_cc-t_all_aux[i_pulse_end])/secyer), cum_m_ej_aux[i_pulse_end], marker='x',s=100, lw=2, color='r', zorder=2)
                            ax.plot([x_start, x_end],[y_start, y_end], lw=2, ls='-', color="#FFAA00")
                            bx.plot([np.log10((t_cc-t_all_aux[i_pulse_start])/secyer),
                                     np.log10((t_cc-t_all_aux[i_pulse_end])/secyer)],
                                    [cum_m_ej_aux[i_pulse_start], cum_m_ej_aux[i_pulse_end]], color="#FFAA00", lw=2, ls='-')
                            i = min(i_pulse_end+1, len(cum_m_ej_aux))
                            m_already_ejected = cum_m_ej_aux[i_pulse_end]
            pinfo_file.close()
            # print "==============="
            # print f, ":", cnt, "min m pulse", mthreshold
            # print "==============="
            ax.set_xlabel(r"$\mathrm{mod\ num}$")
            # bx.set_xlim(-1.15,-1.3)
            # ax.set_ylim(-0001,0.45)
            bx.set_ylabel(r"$\mathrm{Cumulative} \Delta M \ \mathrm{[M_\odot]}$")
            bx.set_xlabel(r"$\log_{10}\{(t_\mathrm{cc} - t) / \mathrm{[years]}\}$")
            bx.invert_xaxis()
            ax.set_ylabel(r"$\Delta M \ \mathrm{[M_\odot]}$")
            ax.set_title(r"$M_\mathrm{He}=$"+str(myFolderSort(f))+"\,$M_\odot$")
            bx.set_title(r"$\#\ \mathrm{pulses}=$"+str(cnt))
            plt.tight_layout()
            try:
                os.system('mkdir -p '+f+'/PLOTS/')
            except:
                pass
            plt.savefig(f+'PLOTS/cnt_pulses'+str(myFolderSort(f))+".png")
            if show_plot:  plt.show()
            plt.close()
        if cnt>0:
            pulses ="PPI+CC"
    return pulses, cnt

def getTthermal(M,R,L,Lnu):
    maxL = max_array(L,Lnu)
    return (G_cgs*M*M*Msun*Msun/(R*Rsun_cm*maxL*Lsun))/secyer


## find BH mass using MESA IV criterion
## BH mass is the mass at which the binding energy integrated from the surface exceeds 10^48 erg/s
## checks also that matter is actually bound to the star.

def getBHmassfromprofile(pfile):
    global Rsun_cm, Msun, G_cgs

    src,col = getSrcCol(pfile)
    v = src[:, col.index("velocity")] #cm/s
    # select only stuff slower than the escape velocity
    try:
        vesc = src[:, col.index("vesc")]
        ind = v[:] < vesc[:]
        if np.sum(ind) == 0: return 0 # PISN => no BH mass
    except: #RUNSTAR3
        if "RUNSTAR3" in pfile:
            m = src[:, col.index("mass")]*Msun
            r = 10**(src[:, col.index("logR")])*Rsun_cm
            vesc = np.sqrt(2*G_cgs*m/r) # cm/s
            ind = v[:] < vesc[:]
        else:
            print(colored("Can't find or calculate v_esc...check getBHmassfromprofile!", "red"))

    # reload things
    r = src[ind, col.index("radius")] #Rsun
    r *= Rsun_cm # in cm
    m = src[ind,col.index("mass")] # Msun
    dm = src[ind, col.index("dq")]*m[0] # Msun
    dm *= Msun # in g
    m *= Msun # in g
    ebind = 0
    for i in range(0, len(m)-1,1):
        ebind = ebind + G_cgs*m[i+1]*dm[i]/r[i]     # standard_cgrav * s%m(k+1) * s%dm(k)/s%r(k)
        if ebind >= 1e48:
            #print i
            M_from_bindingE = m[i]/Msun
            break
    # print colored("max{M(v<vesc)} =", "yellow"), colored(max(m)/Msun,"yellow")
    # print colored("max{M} =", "yellow"), colored(max(src[:,col.index("mass")]),"yellow")
    # print colored("Mbh from binding E=", "yellow"), colored(M_from_bindingE,"yellow")
    # if max(m)/Msun != M_from_bindingE:
    #     print colored("max{M(v<vesc)} != Mbh from binding E","red"), colored("DM=","red"), colored(max(m)/Msun - M_from_bindingE,"red")
    # print "using Mbh from binding energy"
    return M_from_bindingE


def get_Mhe_rem_behavior(f):
    hfile = getHistoryFile(f)
    src, col = getSrcCol(hfile)
    # print col
    ## This is the initial He core mass
    mhe = src[0,col.index("star_mass")] # f.split('/')[-2].split('_')[0] #
    # gamma = src[:, col.index("gamma_integral")]
    # preSNind = np.argmin(np.absolute(gamma-0.005)) #should return the index of the first minimum
    # mhe = src[preSNind, col.index("star_mass")]
    # Tc = 10**(src[:, col.index("log_center_T")])
    # c_ign = np.argmin(np.absolute(Tc - 5e8))
    # try:
    #     mco = src[c_ign, col.index("co_core_mass")] #
    # except:
    #     mco = max(src[c_ign, col.index("o_core_mass")], src[c_ign, col.index("c_core_mass")])
    mco = max(src[:, col.index("co_core_mass")])
    Etot = src[:, col.index("total_energy")]
    mrem = src[:,col.index("star_mass")]
    try:
        pfname = getFinalProfile(f)
        # print pfname
        mrem = getBHmassfromprofile(pfname)
        # print colored(f,"blue")
        # print colored("BH mass from binding energy:"+str(mrem),"blue")
        # pfname = getpfile(f)
        # print pfname
        # mrem = getBHmassfromprofile(f+'LOGS/'+pfname)
        # print colored(f,"blue")
        # print colored("BH mass from binding energy:"+str(mrem),"blue")
    except:
        print(colored("WARNING ======","red"))
        print(colored(f,"red"))
        print(colored("failed to find location for B>1e48 erg...","red"))
        print(colored("will use the total helium core mass as proxy...","red"))
        mrem = 0 #mrem[-1]
    pulses, num_pulses = findPulses_mejection(f, show_plot=False)

    if (pulses=="PISN"):
        color = 'y'
        mrem = 0
    elif (pulses=="CC"):
        color='b'
    elif (pulses=="failed"):
        color='k'
    else: ## PPI + CC
        color = 'g'

    return mhe, mco, mrem, color, pulses

## miscellanea ---------------------------------------------------------------------------------------------

def max_array(a,b):
    # given two arrays of the same length
    # returns an array containing the max in each element
    if len(a)==len(b):
        c = np.zeros(len(a))
        for i in range(len(a)):
            c[i]=max(a[i],b[i])
        return c
    else:
        print("you gave me two array of lengths:",len(a),"=/=",len(b))
        print(colored("can't work with this...going home!","red"))

def min_array(a,b):
    # given two arrays of the same length
    # returns an array containing the max in each element
    if len(a)==len(b):
        c = np.zeros(len(a))
        for i in range(len(a)):
            c[i]=min(a[i],b[i])
        return c
    else:
        print("you gave me two array of lengths:",len(a),"=/=",len(b))
        print(colored("can't work with this...going home!","red"))

def SB_law(r,t):
    # given radius and temperature in solar radii and kelvin, returns the luminosity in solar units
    sigma  = 5.67051e-5 #cgs units
    Rsun = 6.99e10 #cm
    Lsun = 4e33 #erg/s
    r *= Rsun #convert to cm
    l = 4*math.pi*sigma*t**4*r**2
    l = l/Lsun
    return l
