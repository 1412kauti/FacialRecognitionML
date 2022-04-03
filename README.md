# A.I. Attendance System

This desktop application attendance system uses A.I. for facial recognition.
Coding was executed in Pycharm Professional by Jetbrains under the student license code.
To be updated in real-time with changes on the script, version control was used, such as **`pipenv`**, **`git`** and **`Github`**. 
All updates could be done through **`Pycharm`** which has built-in version control.<br>
The application can recognise registered students or workers and track their attendance at any activity.
A.I. Attendance System is a planned project by a team group assigned with the unit ***Agile Project Management*** at 
the  ***University of Bedfordshire***.<br>
The purpose of this project does demonstrate knowledge in project management 
environments such as ***PRINCE2***.
The application is a basic form of attendance tracking of any user of any institute or company. 
Video capture is one of the main functions done by installing specific resourceful libraries. 
Further information is in the Run section.
### For start
The development of this application is coded to accommodate multiple platforms.
The code runs on **`Windows`** and on **`Linux`**. It was debugged on both **`Windows`** **PC** and **Mac**.
For this reason `starter.py`, `Facial.py` are coded for **`Windows`** and `starter2.py`, `Facial2.py` are for **`Mac`**, and `admin.py` is for both.<br>
To properly run the code all dependencies must be installed on the `requirements.txt` file which will be automatically 
installed by `pip` environment using the `Pipfile`.<br>
```
pipenv install
```
On **`Windows`**:<br>
- `dlib` and `opencv` requires other packages to be installed outside **`Pycharm`**:

	**`Visual Studio C++ 2019`** and **`CMake`**

On **`Mac`**:
- `dlib` and `opencv` requires other packages to be installed outside **`Pycharm`**


### Run

After all dependencies installed the following command will run the code. 
For successful run a camera is required, built-in or attached<br>

On **`Windows`**:<br>
```
python starter.py
python admin.py
```

On **`Mac`**:
``` 
python starter2.py
python admin.py
```
