import tempfile
import filecmp
import os.path
import yaml
import pytest
import h5py
import numpy as np
from astropy.io import ascii

EXAMPLE_SIM = os.path.join(os.path.dirname(__file__), 'Mini_N64_L32')
EXAMPLE_SUBSAMPLE_HALOS = os.path.join(os.path.dirname(__file__), 
    'halos_xcom_2_seed600_abacushod_new.h5')
EXAMPLE_SUBSAMPLE_PARTS = os.path.join(os.path.dirname(__file__), 
    'particles_xcom_2_seed600_abacushod_new.h5')
EXAMPLE_GALS = os.path.join(os.path.dirname(__file__), 'LRGs.dat')
path2config = 'config/abacus_hod.yaml'

def test_loading(tmp_path):
    '''Test loading a halo catalog
    '''

    from abacusnbody.hod import prepare_sim
    from abacusnbody.hod.abacus_hod import AbacusHOD

    config = yaml.load(open(path2config))
    sim_params = config['sim_params']
    HOD_params = config['HOD_params']
    power_params = config['power_params']

    simname = config['sim_params']['sim_name'] # "AbacusSummit_base_c000_ph006"
    simdir = config['sim_params']['sim_dir']
    z_mock = config['sim_params']['z_mock']
    savedir = config['sim_params']['subsample_dir']+simname+"/z"+str(z_mock).ljust(5, '0') 

    # check subsample file match
    prepare_sim.main(path2config)

    newhalos = h5py.File(savedir+'/halos_xcom_2_seed600_abacushod_new.h5', 'r')['halos']
    temphalos = h5py.File('halos_xcom_2_seed600_abacushod_new.h5', 'r')['halos']
    for i in range(len(newhalos)):
        assert newhalos[i] == temphalos[i]
    newparticles = h5py.File(savedir+'/particles_xcom_2_seed600_abacushod_new.h5', 'r')['particles']
    tempparticles = h5py.File('particles_xcom_2_seed600_abacushod_new.h5', 'r')['particles']
    for i in range(len(newparticles)):
        assert newparticles[i] == tempparticles[i]

    # additional parameter choices
    want_rsd = HOD_params['want_rsd']
    write_to_disk = HOD_params['write_to_disk']
    bin_params = power_params['bin_params']
    rpbins = np.logspace(bin_params['logmin'], bin_params['logmax'], bin_params['nbins'])
    pimax = power_params['pimax']
    pi_bin_size = power_params['pi_bin_size']
    
    # create a new abacushod object
    newBall = AbacusHOD(sim_params, HOD_params, power_params)
    
    # throw away run for jit to compile, write to disk
    mock_dict = newBall.run_hod(newBall.tracers, want_rsd, write_to_disk = True)
    savedir_gal = config['sim_params']['scratch_dir']\
    +"/"+simname+"/z"+str(z_mock).ljust(5, '0') +"/galaxies_rsd/LRGs.dat"
    data = ascii.read("LRGs.dat")
    data1 = ascii.read(savedir_gal)
    for ekey in data.keys():
        assert abs(np.sum(data[ekey] - data1[ekey])) < 1e-16

