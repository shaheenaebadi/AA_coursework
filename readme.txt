readme.txt - Non-Standard Library Installation Instructions
===========================================================

The following non-standard Python libraries are required for activity_1.4.py.
All other activities (1.1, 1.2, 1.3) use only Python standard libraries.

REQUIRED LIBRARIES
------------------

1. numpy
   Used in: activity_1.4.py
   Install with:
       pip install numpy

2. face_recognition
   Used in: activity_1.4.py
   Install with:
       pip install face_recognition

   Note: face_recognition depends on dlib, which may require additional steps:
   - On Windows, it is recommended to install cmake first:
       pip install cmake
   Then install dlib before face_recognition:
       pip install dlib
       pip install face_recognition

INSTALL ALL AT ONCE
-------------------
    pip install numpy cmake dlib face_recognition

REQUIREMENTS
------------
- Python 3.6 or higher
- pip (Python package manager)

# for 1.4 run - python -W ignore activity_1.4.py
I'm running the script with the -W ignore flag to 
suppress deprecation warnings that come from inside
 the face_recognition_models library. 
 These warnings are not caused by my code —
  they appear because the library internally uses 
  a package called pkg_resources which is being phased 
  out by its developers. Using -W ignore simply hides 
  them so the actual output is easier to read. 
  The program runs identically either way.#