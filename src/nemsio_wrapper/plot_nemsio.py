'''
    Author: Christina Holt
    Date:   May 2018

    Description:
        Utilizes the Python-wrapped NCEP nemsio library to read a nemsio
        formatted file and generages plots saved as png files for regularly
        spread atmospheric levels for several standard atmospheric variables.
        Specifically, surface pressure, temperature, U and V wind components,
        wind speed, and specific humidity. These are controlled in main() below
        with the variable:

            varnames = ['psfc', 'tmp', 'ugrd', 'vgrd', 'wind', 'spfh']

    Usage: python plot_nemsio.py -h

'''
from __future__ import print_function

import argparse
import math
from functools import partial
from multiprocessing import Pool

import numpy
import matplotlib.pyplot as plt
from   mpl_toolkits.basemap import Basemap

import nemsio_wrapper as nw

plt.switch_backend('Agg')

def titles(varname, lev, dscrpt=''):
    ''' Set titles for variables.'''

    ctitles = {
        'pres':  'Level {lev} Surface Pressure {description} (Pa)',
        'dpres': 'Level {lev} DPressure {description} (Pa)',
        'tmp':   'Level {lev} Temperature {description} (K)',
        'ugrd':  'Level {lev} Zonal Wind {description} (m s-1)',
        'vgrd':  'Level {lev} Meridional Wind {description} (m s-1)',
        'spfh':  'Level {lev} Specific Humidity {description} (kg kg-1)',
        'wind':  'Level {lev} Wind Speed {description} (m s-1)'
        }
    return ctitles.get(varname).format(lev=lev, description=dscrpt)


def get_field(fn, varname, level_type, lev):
    ''' Read nemsio data from file given a variable name (varname, and a level type (varlev).'''
    dimx, dimy = nw.get_nemsio_dims(fn)
    return nw.read_nemsio_wrapper(fn, varname, level_type, lev, dimx, dimy)

def contours(varname, incvar, lev):
    ''' Set contour levels and colorbar ticks based on the field. '''

    # Get the min/max of the field to be plotted
    mnval = incvar.min()
    mxval = incvar.max()

    # It's helpful to see the min/max values as the program runs.
    print("Min/max for ", varname, "at Level ", lev, ": ", mnval, ", ", mxval)

    # The desired number of contour levels to use
    nticks = 10

    # Find the maximum absolute value of the min or max
    cmap_mxval = max(abs(mnval), mxval)
    cmap_mxval = math.ceil(cmap_mxval) if abs(cmap_mxval) > 1 else cmap_mxval


    # If the range includes negative numbers, center the contouring on zero by setting minval
    # to opposite of mxval, otherwise the min is zero.
    cmap_mnval = -1.0*cmap_mxval if mnval < 0 else mnval
    cmap_mnval = math.floor(cmap_mnval) if abs(cmap_mnval) > 1 or abs(cmap_mxval) > 1 else cmap_mnval


    # --- Calculate the contour levels ---
    cmap_valint = (cmap_mxval - cmap_mnval) / float(256)                  # Interval
    clevs = list(numpy.arange(cmap_mnval, cmap_mxval, cmap_valint)) + [cmap_mxval]    # List of levels

    # --- Calculate the ticks on the colorbar ---

    # Calculate colorbar tick interval
    cint = (cmap_mxval-cmap_mnval)/float(nticks)

    # List of all the values from min to max to the list, inclusive
    ctcks = list(numpy.arange(cmap_mnval, cmap_mxval, cint)) + [cmap_mxval]

    return ctcks, clevs

def make_plot(varlevs, args):
    ''' Plot nemsio field gevn a variable, the command line args, and a level. '''

    var, lev = varlevs

    lev = int(lev) # Level should be an integer

    # Set the level type and varname (if different)
    if var == 'psfc':
        varlev = 'sfc'
        varname = 'pres'  # Renaming here bc pressure could be at levels other than surface.
    else:
        varlev = 'mid layer'
        varname = var

    # Retrieve the requested field from the nemsio file.
    if varname == 'wind':
        lats, lons, u = get_field(args.fnames[0], 'ugrd', varlev, lev)
        lats, lons, v = get_field(args.fnames[0], 'vgrd', varlev, lev)
        incvar = numpy.sqrt((u*u)+(v*v))
    else:
        lats, lons, incvar = get_field(args.fnames[0], varname, varlev, lev)

    # Set some figure values
    cmap = 'rainbow'                   # Color map
    ctitle = titles(varname, lev)           # Figure title

    if len(args.fnames) > 1:
        if varname == 'wind':
            lats, lons, u = get_field(args.fnames[1], 'ugrd', varlev, lev)
            lats, lons, v = get_field(args.fnames[1], 'vgrd', varlev, lev)
            field2 = numpy.sqrt((u*u)+(v*v))
        else:
            lats, lons, field2 = get_field(args.fnames[1], varname, varlev, lev)
        incvar = incvar - field2
        cmap = 'seismic'
        ctitle = titles(varname, lev, 'Increment')         # Figure title

    # Set color intervals and contour levels based on the data to be plotted
    ctcks, clevs = contours(varname, incvar, lev)

    # Generate the name of the output file
    if args.ofile_base:
        filename = '%s.%s_lev%02d.png'%(args.ofile_base, varname, (lev))
    else:
        filename = '%s_lev%02d.png'%(varname, (lev))


    # --- Plot the field on a map ---

    # Set up a standard blank map
    basemap = Basemap(projection='mill', urcrnrlon=lons.max(), urcrnrlat=lats.max(),
                      llcrnrlon=lons.min(), llcrnrlat=lats.min(), lon_0=0.0)

    # Map the field's lats/longs to basemap x, y coordinates
    (x, y) = basemap(lons, lats)

    # Add the meteorological field (incvar) as filled contours to the blank map
    basemap.contourf(x, y, incvar, levels=clevs, cmap=cmap)


    # Add some lat/lon lines for easy geographic reference
    parallels = [-75, -45, -15, 15, 45, 75]
    meridians = [30, 90, 150, 210, 270, 330]
    basemap.drawparallels(parallels, labels=[True, True, True, True], linewidth=0,
                          fontsize=10)
    basemap.drawmeridians(meridians, labels=[True, True, True, True], linewidth=0,
                          fontsize=10)

    # Add coastlines to the map
    basemap.drawcoastlines(linewidth=0.5)

    # Set location of colorbar
    cax = plt.axes([0.1, 0.01, 0.8, 0.05])
    #cax = plt.axes([0.1, 0.01, 0.05, 0.8])

    # Add a colorbar with the pre-computed tick marks (from contours function)
    fmt = '%.2f' if abs(max(ctcks)) > 1 else '%.2E'
    cbar = plt.colorbar(cax=cax, ticks=ctcks, orientation='horizontal',
                        format=fmt)

    # Add a title to the figure
    cbar.set_label(ctitle)

    # Change size of colorbar labels
    cbar.ax.tick_params(labelsize=6)

    # Set some parameters for saving the figure nicely
    savefig_dict = {'transparent':False, 'dpi':300, 'bbox_inches':'tight'}

    # Save the figure and close the plot
    plt.savefig(filename, **savefig_dict)
    plt.close()


def parse_args():
    ''' Define the command line arguments. '''
    parser = argparse.ArgumentParser(prog='plot_nemsio')
    parser.add_argument('-f', '--fnames',
                        nargs='+', required=True,
                        help="Filename(s) to plot. Providing two will plot the difference.")
    parser.add_argument('-o', '--ofile_base',
                        default=False,
                        help="String to include in the output filename")
    parser.add_argument('-p', '--numprocs',
                        default=1,
                        help="Number of processors to use")
    parser.add_argument('-l', '--lev_freq',
                        default=1,
                        help="Frequency of levels to plot, i.e. '-l 4' plots every 4th level")
    return parser.parse_args()


def main():
    '''Given command-line arguments, plot nemsio fields for standard variables.'''

    # Parse command line arguments
    args = parse_args()

    # Define the meteorological variables to plot.
    varnames = ['psfc', 'tmp', 'ugrd', 'vgrd', 'wind', 'spfh']

    # Define number of model levels.
    top_lev = 64
    all_levels = range(1, top_lev+1, int(args.lev_freq))

    # Set up multiprocessing pool
    pool = Pool(int(args.numprocs))

    # Loop through all variables to plot, and add them to the zipped list
    var_lev = []
    for var in varnames:
        if var != 'psfc':
            rep_var = [var] * len(all_levels)
            var_lev = var_lev + zip(rep_var, all_levels)
        else:
            var_lev = var_lev + zip([var], '1')

    # Add a process to the pool for every var/level combo
    pool.map(partial(make_plot, args=args), var_lev)
    pool.close()
    pool.join()

if __name__ == "__main__":
    main()
