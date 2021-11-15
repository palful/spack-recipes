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

Here an example on how to use them:
```
spack install yambo@5.0.4%gcc@11.2.0 +mpi +openmp linalg=parallel profile=memory,time ^intel-mkl ^hdf5@1.12.0
```
With this command you are asking spack to install Yambo at v5.0.4 using GCC compiler at v11.2.0, enabling both MPI and OpenMP parallelization, enabling parallel (ScaLAPACK) linear algebra and the profiling for memory and time. In addition you are specifing to use Intel-MKL library for lapack, HDF5 at v1.12.0.

### Installing on MacOS

For MacOS users it is suggested to install Yambo with the GCC compiler, but using CMake compiled with the Clang compiler:
```
spack install yambo@5.0.4%gcc@11.2.0 +mpi +openmp profile=memory,time ^cmake%apple-clang
```
