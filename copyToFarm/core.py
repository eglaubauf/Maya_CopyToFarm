#####################################
#LICENSE                            #
#####################################
#
# Copyright (C) 2019  Elmar Glaubauf
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import maya.cmds as cmds
import fastCopy as fc
import re

class Core():

    def __init__(self):
        self.ws = self.getWorkspace()
        self.files = []
        self.copyAll = True
        self.dest = ''
        self.OpenNew = False
        self.ImportFlag = False
        self.count = 0

    # Query the Current Workspace
    def getWorkspace(self):  
        return cmds.workspace(q=True, directory=True, rd = True)
    
    # Gets a List of all Files in a Maya Scene
    def getAllLinkedFiles(self):
        self.files = cmds.file(query=1, list=1, withoutCopyNumber=1)   
        return self.files

    # Set the New Destination
    def setDestination(self, newDest):            
        self.dest = newDest
        return True

    #Sets the Workspace to the New Directory
    def setNewWorkspace(self):
        cmds.workspace(self.dest, openWorkspace=True)

    #Set all Files to Copy
    def setCopyAll(self, flag):
        self.copyAll = flag

    #Set to Copy only newer Files
    def setOpenNew(self, flag):
        self.OpenNew = flag

    #Set to Copy only newer Files
    def setImport(self, flag):
        self.importFlag = flag

    #Import all Levels of References 
    def importReference(self):
        changed = True
        count = 0
        while changed is True: #Call As long as there is a Change
            changed = False
            references = cmds.file(q=True, r=True)
            if references is not None: 
                for r in references:
                    cmds.file(r, ir=True)
                    changed = True
                    count +=1
        self.saveFileAppend('_imported')
        return count    

    #Copies all Files to a new Workspace
    def copyFiles(self):
        self.count = 0

        #Get all Tex/Filenodes in Scene
        nodes = cmds.ls()
        #For each Node get all Attrs and check if string matches
        for n in nodes:
            for attr in cmds.listAttr(n, r=1):
                parm =  n+'.'+attr
                if cmds.objExists(parm):
                    try:
                        #Get Attr cant handle certain datatypes
                        aType = cmds.getAttr(parm, typ=1)
                    except:
                        #but lets ignore the exeception and continue onwards
                        continue
                    if  aType == 'string':
                            val = cmds.getAttr(parm)
                            if val is not None:
                                for f in self.files:

                                    destination = self.calcDestination(f)
                                    occur = f.rfind("/")
                                    sourceFile = f[occur+1:]
                                    #Check for Match
                                    if val.endswith(sourceFile):
                                        #CopyFile
                                        self.copy(f, destination)
                                        #ChangeAttribute
                                        cmds.setAttr(parm, destination,type="string")
                                        self.files.remove(f)
                                        self.count+=1
                                   
        #Copy References (only non .ma /.mb)
        self.copyReference()

        #copySceneFile (Save File into new location)
        f = self.files[0]
        destination = self.calcDestination(f)
        cmds.file( rename=destination )
        cmds.file( save=True, type='mayaAscii' )

        self.count+=1
        return self.count


    def copyReference(self):

        for f in self.files:
            if not f.endswith('.ma') and not f.endswith('.mb'):
                
                destination = self.calcDestination(f)
                #Remove double Slashes
                destination = re.sub('//+', '/', destination)
                #Get Reference Node
                rn = cmds.referenceQuery(f ,rfn=True)
                #Copy File
                self.copy(f,destination)
                #Relink Reference
                cmds.file(destination, loadReference=rn)
                

    def copy(self, f, destination):

        #Copy only Newer Files?
        if self.copyAll is False:
            if os.path.exists(destination):
                if os.path.getctime(f) > os.path.getctime(destination) is True:
                    try:
                        fc.copyfile(f, destination)
                    except:
                        return 0
                    self.count += 1
        else: 
            try:
                fc.copyfile(f, destination)
                self.count += 1
            except:
                return 0

    
    def calcDestination(self, f):
        
        occur = f.rfind("/")
        #Full Paths from SourceFile
        sourceFile = f[occur+1:]
        sourcePath = f[:occur+1]
        sourcePathSub = ''
        
        #Trim away Project Directory
        if sourcePath.startswith(self.ws) is True:
            sourcePathSub = sourcePath[len(self.ws):]
        else:
            occur = sourcePath.find('/')
            sourcePathSub = sourcePath[occur:]
        
        # create Directories if Missing
        destinationPath = self.dest + '/' + sourcePathSub
        if not os.path.exists(destinationPath):
            try:
                os.makedirs(destinationPath)
            except WindowsError:
                return 0
                
        #Return Destination
        return self.dest + '/' + sourcePathSub + sourceFile      

    #Reopens The File in the New Workspace
    def reOpenFile(self):
        self.saveFile()
        
        filepath = cmds.file(q=True, sn= True)
        # Get Folders inbetween Project and SceneFile to be able to open the copied file on the new location
        f = filepath[len(self.ws):]
        f = f[:f.rfind('/')+1]        
        filepath = self.dest + '/' +  f + cmds.file(q=True, sn= True, shn=True)
        cmds.file( filepath , open=True )

    #Save Current File
    def saveFile(self):
        cmds.file(save=True)

    #Save current file with a String appended
    def saveFileAppend(self, suffix):
        filepath = cmds.file(q=True, sn= True)[:-3] + suffix
        cmds.file(rename = filepath)
        cmds.file(save=True)

 

            
            





