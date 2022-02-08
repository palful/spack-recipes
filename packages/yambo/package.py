# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Yambo(AutotoolsPackage, CudaPackage):
    """YAMBO is an open-source code released within the GPL licence.

    YAMBO implements Many-Body Perturbation Theory (MBPT) methods
    (such as GW and BSE) and Time-Dependent Density Functional Theory
    (TDDFT), which allows for accurate prediction of fundamental
    properties as band gaps of semiconductors, band alignments, defect
    quasi-particle energies, optics and out-of-equilibrium properties
    of materials.

    The code resorts to previously computed electronic structure,
    usually at the Density Functional Theory (DFT) level and for this
    reason it is interfaced with two of the most used planewave DFT
    codes used in scientific community, Quantum ESPRESSO and Abinit.
    """

    homepage = "http://www.yambo-code.org/index.php"
    url = "https://github.com/yambo-code/yambo/archive/5.0.4.tar.gz"
    git = "git@github.com:yambo-code/yambo-devel.git"

    maintainers = ['nicspalla']

    version('develop', branch='develop')
    version('5.0.4', sha256='1841ded51cc31a4293fa79252d7ce893d998acea7ccc836e321c3edba19eae8a')
    version('5.0.3', sha256='7a5a5f3939bdb6438a3f41a3d26fff0ea6f77339e4daf6a5d850cf2a51da4414')
    version('5.0.2', sha256='a2cc0f880dd915b47efa0d5dd88cb94edffbebaff37a252183efb9e23dbd3fab')
    version('5.0.1', sha256='bbdbd08f7219d575a0f479ff05dac1f1a7b25f7e20f2165abf1b2cf28aedae92')
    version('5.0.0', sha256='b1cbc0b3805538f892b2b8691901c4cc794e75e056a4bd9ad9cf585899cf0aa9')
    version('4.5.3', sha256='04f89b5445d35443325c071784376c7b5c25cc900d1fdcc92971a441f8c05985')
    version('4.5.2', sha256='0b4f8b82c1d37fce472228bdffb6f6f44b86104d170677a5d55e77a2db832cf0')
    version('4.5.1', sha256='6ef202535e38f334a69bd75bd24ff8403b0a4c6b8c60a28b69d4b1c5808aeff5')
    version('4.5.0', sha256='c68b2c79acc31b3d48e7edb46e4049c1108d60feee80bf4fcdc4afe4b12b6928')
    version('4.4.1', sha256='2daf80f394a861301a9bbad559aaf58de283ce60395c9875e9f7d7fa57fcf16d')
    version('4.3.3', sha256='790fa1147044c7f33f0e8d336ccb48089b48d5b894c956779f543e0c7e77de19')
    # version('4.2.5', sha256='9df63af4c6445434f45b124e0e9d3a20a090d1f0f821bb55fd51ab5a4dccf5ac')

    patch('hdf5.patch', sha256='b9362020b0a29abec535afd7d782b8bb643678fe9215815ca8dc9e4941cb169f', when='@4.3:')
    patch('hdf5_old.patch', sha256='c1ce59d15ab30b33fa474fa58404344254c4203d1762316e178a19cc3a9993b6', when='@:4.2.99')
    patch('iotk_url.patch', sha256='73d1be69002c785bdd2894a3504da06f440e81f07f7356cd52079f287be6d2b9', when='@:4.5.0')

    # MPI + OpenMP parallelism
    variant('mpi', default=True, description='Enable MPI support')
    variant('openmp', default=False, description='Enable OpenMP support')
    depends_on('mpi', when='+mpi')
    depends_on('openmpi@3', when='+mpi %nvhpc')

    # Linear algebra
    variant('linalg', default='none', values=('none', 'parallel', 'slepc'), multi=False,
            description="""Activate additional support for linear algebra:
"parallel" uses SCALAPACK and "slepc" is used for diagonalization of BSE""")
    conflicts('linalg=parallel', when='~mpi',
              msg="Parallel linear algebra available only with +mpi")
    conflicts('linalg=slepc', when='@:4.2.2',
              msg="SLEPc support for linear algebra available only from yambo@4.3.3")
    depends_on('blas')
    depends_on('lapack')
    depends_on('netlib-lapack%nvhpc', when='%nvhpc')
    depends_on('scalapack', when='linalg=parallel')
    depends_on('petsc+mpi+double+complex', when='linalg=slepc +mpi+dp')
    depends_on('petsc~mpi~double+complex~superlu-dist', when='linalg=slepc ~mpi~dp')
    depends_on('petsc~mpi+double+complex', when='linalg=slepc ~mpi+dp')
    depends_on('petsc+mpi~double+complex~superlu-dist', when='linalg=slepc +mpi~dp')
    depends_on('slepc', when='linalg=slepc')
    depends_on('slepc@:3.7.4', when='@:4.5.3 linalg=slepc')

    # GPU acceleration
    conflicts('cuda_arch=none', when='+cuda',
              msg="CUDA architecture is required when +cuda")
    conflicts('@:4.5.3', when='+cuda',
              msg="CUDA-Fortran available only from version 5.0.0")
    conflicts('%gcc', when='+cuda',
              msg="CUDA-Fortran available only with NV or PGI compilers")
    conflicts('%intel', when='+cuda',
              msg="CUDA-Fortran available only with NV or PGI compilers")

    # Other variants
    variant('dp', default=False, description='Enable double precision')
    variant('profile', values=any_combination_of('time', 'memory'),
            description='Activate profiling of specific sections')

    # FFTW
    depends_on('fftw-api@3~mpi', when='~mpi')
    depends_on('fftw-api@3+mpi', when='+mpi')

    # HDF5
    variant('parallel_io', default=False, when='@4.4.0: +mpi', description='Activate the HDF5 parallel I/O')
    depends_on('hdf5+fortran+hl~mpi', when='@:4.4.0')
    depends_on('hdf5+fortran+hl~mpi', when='~parallel_io')
    depends_on('hdf5+fortran+hl+mpi', when='+parallel_io')

    # NETCDF
    depends_on('netcdf-c~mpi', when='~parallel_io')
    depends_on('netcdf-c+mpi', when='+parallel_io')
    depends_on('netcdf-fortran')

    # LIBXC
    depends_on('libxc@2.0.3:3.0.0', when='@:5.0.99')
    depends_on('libxc@5.0:', when='@5.0.99:')

    build_targets = ['ext-libs', 'yambo', 'interfaces', 'ypp']

    parallel = False

    # The configure in the package has the string 'cat config/report'
    # hard-coded, which causes a failure at configure time due to the
    # current working directory in Spack. Fix this by using the absolute
    # path to the file.
    @run_before('configure')
    def filter_configure(self):
        report_abspath = join_path(self.build_directory, 'config', 'report')
        filter_file('config/report', report_abspath, 'configure')

    def enable_or_disable_time(self, activated):
        return '--enable-time-profile' if activated else '--disable-time-profile'  # noqa: E501

    def enable_or_disable_memory(self, activated):
        return '--enable-memory-profile' if activated else '--disable-memory-profile'  # noqa: E501

    def enable_or_disable_openmp(self, activated):
        return '--enable-open-mp' if activated else '--disable-open-mp'

    def enable_or_disable_parallel_io(self, activated):
        return '--enable-hdf5-par-io' if activated else '--disable-hdf5-par-io'

    def configure_args(self):
        spec = self.spec

        if 'intel' in spec['mpi'].name:
            env['MPICC'] = 'mpiicc'
            env['MPICXX'] = 'mpiicpc'
            env['MPIF77'] = 'mpiifort'
            env['MPIFC'] = 'mpiifort'
        if spec['mpi'].name == 'openmpi':
            env['MPICC'] = spec['mpi'].mpicc
            env['MPICXX'] = spec['mpi'].mpicxx
            env['MPIF77'] = spec['mpi'].mpif77
            env['MPIFC'] = spec['mpi'].mpifc
        if '%nvhpc' in spec:
            env['MPICC'] = "mpicc"
            env['MPICXX'] = "mpicxx"
            env['MPIF77'] = "mpif77"
            env['MPIFC'] = "mpif90"
            env['FPP'] = "nvfortran -Mpreprocess -E"
            env['FC'] = "nvfortran"
            env['F77'] = "nvfortran"
            env['CC'] = "nvc"
            env['CPP'] = "cpp -E"
            env['F90SUFFIX'] = ".f90"

        args = [
            '--enable-msgs-comps',
            '--disable-keep-objects',
            '--with-editor=none'
        ]

        # For versions up to 4.5.3 there are hard-coded paths that make
        # the build process fail if the target prefix is not the
        # configure directory
        if '@:4.5.3' in spec:
            args.append('--prefix={0}'.format(self.stage.source_path))
            if '%gcc@9.0.0:' in spec:
                args.append('FCFLAGS=-fallow-argument-mismatch')

        # Double precision
        args.extend(self.enable_or_disable('dp'))

        # Application profiling
        args.extend(self.enable_or_disable('profile'))

        # MPI + threading
        args.extend(self.enable_or_disable('mpi'))
        args.extend(self.enable_or_disable('openmp'))

        # Parallel I/O
        if '@4.4.0:' in spec:
            args.extend(self.enable_or_disable('parallel_io'))

        # Linear Algebra
        if 'linalg=parallel' in spec:
            args.extend([
                '--enable-par-linalg',
                '--with-blacs-libs={0}'.format(spec['scalapack'].libs),
                '--with-scalapack-libs={0}'.format(spec['scalapack'].libs),
            ])
        elif 'linalg=slepc' in spec:
            args.extend([
                '--enable-slepc-linalg',
                '--with-petsc-path={0}'.format(spec['petsc'].prefix),
                '--with-slepc-path={0}'.format(spec['slepc'].prefix),
            ])

        args.extend([
            '--with-blas-libs={0}'.format(spec['blas'].libs),
            '--with-lapack-libs={0}'.format(spec['lapack'].libs)
        ])

        # I/O
        args.extend([
            '--with-netcdf-path={0}'.format(spec['netcdf-c'].prefix),
            '--with-netcdff-path={0}'.format(spec['netcdf-fortran'].prefix),
            '--with-hdf5-path={0}'.format(spec['hdf5'].prefix)
        ])

        # Other dependencies
        args.append('--with-fft-path={0}'.format(spec['fftw-api'].prefix))
        args.append('--with-libxc-path={0}'.format(spec['libxc'].prefix))

        # CUDA
        if '+cuda' in spec:
            enable_cuda = '--enable-cuda=cuda{0}.{1}'.format(*spec['cuda'].version)
            for cc in spec.variants['cuda_arch'].value:
                enable_cuda += ',cc{0}'.format(cc)
            args.append(enable_cuda)

        return args

    def install(self, spec, prefix):
        # 'install' target is not present
        install_tree('bin', prefix.bin)
