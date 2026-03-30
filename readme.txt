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
