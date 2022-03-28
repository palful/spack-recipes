# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyYambopy(PythonPackage):
    """Yambopy creates automatic workflows for yambo and quantum espresso using python. 
Do pre/post-processing, data analysis and plotting for yambo and quantum espresso."""

    homepage = "http://www.yambo-code.org/wiki/index.php?title=First_steps_in_Yambopy"
    url      = "https://github.com/yambo-code/yambopy/archive/refs/tags/v0.1.tar.gz"

    maintainers = ['nicspalla', 'palful']

    version('0.1', sha256='36eb12bbbfd36bdf5e5a8bc9738db4f576e6692c04341362cc1f9f3cf63b2423')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-netcdf4~mpi^hdf5~mpi+fortran', type=('build', 'run'))
    depends_on('py-matplotlib backend=tkagg', type=('build', 'run'))
    depends_on('py-abipy', type=('build', 'run'))
    depends_on('py-lxml', type=('build', 'run'))
    #depends_on('netcdf-c~mpi', type=('build', 'run'))
    #depends_on('hdf5~mpi', type=('build', 'run'))
