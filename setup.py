from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

setup(
    name="piconumpy",
    packages=find_packages(exclude=["bench"]),
    extras_require={
        "dev": ["transonic", "numpy", "pytest", "pythran"],
        # black can't be installed with PyPy3!
        "full": ["black"],
    },
    # you need to manually install hpy.devel from the git repo for now
    setup_requires=["hpy.devel>=0.0.0"],
    ext_modules=[
        Extension(
            "piconumpy._piconumpy_cpython_capi",
            ["piconumpy/_piconumpy_cpython_capi.c"],
            extra_compile_args=[
                "-Wfatal-errors",  # stop after one error (unrelated to warnings)
                "-Werror",  # turn warnings into errors (all, for now)
            ],
        ),
        *cythonize("piconumpy/_piconumpy_cython.pyx"),
    ],
    hpy_ext_modules=[
        Extension(
            "piconumpy._piconumpy_hpy",
            ["piconumpy/_piconumpy_hpy.c"],
            extra_compile_args=[
                # see https://github.com/hpyproject/hpy/issues/219
                # '-Wfatal-errors',
                # '-Werror',
            ],
        ),
    ],
)
