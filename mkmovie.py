#!/usr/bin/env python

import glob
import os
import sys


def renumber(folder):
    files = glob.glob(folder+"*.png")
    i = 0
    for f in files[::-1]:
        os.system('mv '+f+' '+folder+'/frame%06d' % i+'.png')
        # print 'mv '+f+' '+folder+'/frame%06d' % i+'.png'
        i += 1


def ffmpeg(folder, frame_rate=10, outname='out.avi'):
    # os.system('ffmpeg -r 10 -i '+folder+'/frame%06d.png '+str(outname))
    os.system('ffmpeg -r '+str(frame_rate)+' -i '+folder+'/mix_%04d.png '+str(outname))
    # os.system('ffmpeg -r 10 -i '+folder+'/mix*.png '+str(outname))
    print("done!")



if __name__ == "__main__":
    folder = sys.argv[1]
    outname = sys.argv[2]
    if len(sys.argv>2):
        frame_rate = sys.argv[3]
    print(sorted(glob.glob(folder+"/*.png")))
    mv = input("Does "+folder+" png content need renumbering? [Y/n]")
    if ((mv == "Y") or (mv == "y")):
        renumber(folder)
    print("Now making the movie...")
    ffmpeg(folder, outname=outname)
