# Import libraries
import numpy 
from distutils.core import setup
from Cython.Build import cythonize
import Cython.Compiler.Options 
Cython.Compiler.Options.annotate = True  # Enable annotation for better understanding


# Setup configuration for Cython compilation
setup(
    ext_modules = cythonize("sobel_cycode.pyx", annotate=True),  # Cythonize the .pyx file and enable annotation
    include_dirs=[numpy.get_include()]  # Include NumPy header files
)
