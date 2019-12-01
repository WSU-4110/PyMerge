from distutils.core import setup

try:
    from Cython.Build import cythonize
except ImportError as err:
    print(f"Please install Cython to regenerate the DLL: {err}")


# Run python3 setup.py build_ext --inplace
setup(
    name="cython_accelerator/lcs_cython",
    ext_modules=cythonize("lcs_cython.pyx"),
)
