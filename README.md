# Maya_CopyToFarm

This script provides a window in which the user is able to select a directory to copy the current file and it´s dependencies to a different, arbitrary location (e.g. a network storage). In this process the script will copy all linked/referenced files to the chosen location as long as they are below the current workspace. 

The addon also provides the user with a list of files which will be copied. The script is optmized for fast copying and copies only the files which are referenced or linked to within Maya.  Further the user is able to import all reference (also multi-level references) with one click. In this case the script saves the current file as a copy with a "_imported" suffix. 

The user can also choose if only newer files or all files should be copied. In both cases existing files will be overwritten. 

The user is also able to open the File in its destination folder in one step, by setting the according checkmark. 

This script has only been tested with Maya 2019 and Windows 10. 


![alt text](https://github.com/eglaubauf/Maya_CopyToFarm/blob/master/images/Screenshot.png "The Provided UI by the Script")


## Features
- Copy Files to different Location (Links included)
- Import all References (and create a backup from it)
- List all Linked files
- Only copy newer files
- Copy all Files
- Open New File in one Step (also sets the Workspace to this new Location)
- Copy Files from the current Project to new Project Directory (Rebuilds FolderStructure Below the new Project Location)
- works with Maya 2019 and newer (2018 and older possibly as well but untested)
- OS-Exceptions are handled
- Windows only (at the Moment)


## Todos

- A possible Version for Linux/OSX (low Priority)
- Cannot copy files from outside Mayas Project Dir for now since the API is a bit of a PITA sometimes (on it...)

## Installation

1. Download zip or clone repo
2. Copy the Folder "CopyToFarm" to your "C:\Users\<User>\Documents\maya\2019\scripts" Folder
3. Add provided Shelf or add Lines below to a shelf button:

```
import copyToFarm.controller as copyToFarmCtrl
reload(copyToFarmCtrl)
copyToFarmCtrl.open()
```