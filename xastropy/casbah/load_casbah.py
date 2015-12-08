""" Module for buildling CASBAH galaxy database
"""
from __future__ import print_function, absolute_import, division, unicode_literals

from astropy.table import Table

#from astropy import constants as const
from xastropy.casbah import galaxy_data as xcgd
from xastropy.casbah import utils as xcasbahu
from xastropy.xutils import lists as xxul
from xastropy.cgm import field as xcgmf
from xastropy.obs import radec as xra

from xastropy.xutils import xdebug as xdb


# SDSS
def load_field(field):
    """ Load up CASBAH data for a given field

    Parameters:
    -----------
    field: tuple
      (Name, ra, dec)

    Returns:
    --------
    lfield:
      Loaded IgmGalaxyField class
    """
    reload(xcgmf)
    reload(xcasbahu)
    lfield = xcgmf.IgmGalaxyField(field[0], (field[1],field[2]))

    # Load targets
    targ_file = xcasbahu.get_filename(field,'TARGETS')
    lfield.targets = Table.read(targ_file,delimiter='|',
        format='ascii.fixed_width',
        fill_values=[('--','0','MASK_NAME')])

    # Load observing details for multi-object follow-up
    obs_file = xcasbahu.get_filename(field,'MULTI_OBJ')
    lfield.observing = Table.read(obs_file,delimiter='|',
        format='ascii.fixed_width',
        fill_values=[('--','0','DATE_OBS','TEXP')])

    # Load galaxies
    sdss_file = xcasbahu.get_filename(field,'SDSS')
    sdss_tab = Table.read(sdss_file)
    # VSTACK
    hectospec_file = xcasbahu.get_filename(field,'HECTOSPEC')

    lfield.galaxies = sdss_tab

    # Return
    return lfield
