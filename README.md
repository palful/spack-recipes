# my-repo
Contains definitions for custom spack packages.

## Download

```
git clone https://github.com/nicspalla/my-repo.git <repo_name>
```
please replace the string <repo_name> here below and following with a name useful for you.

## Requirements

- spack version 0.16+
  - [spack system requirements](https://spack.readthedocs.io/en/latest/getting_started.html)

### Software suggested but not required

- GCC compilers suite version 9.0+
  - installable with spack:
    ```
    spack install gcc@11.2.0
    spack compiler add $(spack location -i gcc@11.2.0)
    ```

## Repository installation

```
spack config --scope user edit repos
```
then add the following two lines:
```
repos:
- /path/to/<repo_name>
```
please replace `/path/to/<repo_name>` with the complete path of this repository.

## Yambo installation

### Default installation
```
spack install yambo
```
This command will install the latest stable version of Yambo, with MPI enabled, using the spack preferred versions of the required libraries (openmpi, hdf5, netcdf-c, netcdf-fortran, fftw, libxc, lapack).

### Variants and library specifications
```
spack info yambo
```
This command displays the list of the supported versions of Yambo and the list of variants available.

Here a list of commands that will lead to a good installation of Yambo starting from the installation of Spack:
```
git clone https://github.com/nicspalla/my-repo.git $HOME/my-repo
git clone https://github.com/spack/spack.git $HOME/spack
cd $HOME/spack
git checkout releases/v0.18
. $HOME/spack/share/spack/setup-env.sh 
spack external find
spack install gcc@11.2.0 && spack compiler add $(spack location -i gcc@11.2.0)
printf "repos:\n  - $HOME/my-repo\n" > $HOME/.spack/repos.yaml
spack install yambo %gcc@11.2.0 +mpi +openmp profile=time,memory
```

Now you can load the Yambo package and check if it works:
```
spack load yambo
yambo -h
```

### Installing on accelerated machines

Here an example of command installation of Yambo supporting acceleration with CUDA-Fortran on a workstation with NVidia Titan V devices (cc70):
```
spack install yambo@5.1.1+cuda-fortran+mpi+openmp+parallel_io+ph+rt+sc+nl cuda_arch=70 linalg=parallel,slepc %nvhpc
```

### Installing on MacOS

For MacOS users it is suggested to install Yambo with the GCC compiler, but using CMake compiled with the Clang compiler:
```
spack install yambo@5.1.1%gcc@11.2.0 +mpi +openmp profile=memory,time ^cmake%apple-clang
```
