##MIT License
##
##Copyright (c) 2018 David Riseborough
##
##Permission is hereby granted, free of charge, to any person obtaining a copy
##of this software and associated documentation files (the "Software"), to deal
##in the Software without restriction, including without limitation the rights
##to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
##copies of the Software, and to permit persons to whom the Software is
##furnished to do so, subject to the following conditions:
##
##The above copyright notice and this permission notice shall be included in all
##copies or substantial portions of the Software.
##
##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##SOFTWARE.

from pathlib import Path
import shutil
import msvcrt
import file_parser
ThisPackPath = Path().resolve()
DataPacksPath = ThisPackPath.parent
OutDirList = list(ThisPackPath.glob("*.outdir"))

print("Datapack parser version 0.5.\n"+\
      "============================\n"+\
      "This script creates a \"release\" version of the current datapack folder\n"+\
      "(where this script is located).\n"+\
      "It automatically replaces scoreboard variables and tags with \"obfuscated\" text\n"+\
      "with a unique prefix for each namespace as determined by configuration files.\n")
bCreateOutput = True
if len(OutDirList)==0:
    print("Output path not identified. (no <dir name>.outdir file) Checking paths only...")
    bCreateOutput = False
elif len(OutDirList)>1: print("More than one output directory identified. Only using one!")
OutPackStr = OutDirList[0].stem
OutPackPath = DataPacksPath / OutPackStr


#If Create Output enabled, create output path
if bCreateOutput:
    if OutPackPath.exists():
        print("The target path "+str(OutPackPath)+" already exists. Checking paths only...")
        bCreateOutput = False
    else:
        OutDataPath = OutPackPath / "data"
        OutDataPath.mkdir(parents=True,exist_ok=True)
        McMetaPath = ThisPackPath / "pack.mcmeta"
        if McMetaPath.is_file():
            shutil.copy(str(McMetaPath),str(OutPackPath))
        else:
            print("WARNING: pack.mcmeta not present")


PrefixMap = {}
PathList = []
ThisDataPath = ThisPackPath / "data"
if ThisDataPath.exists():    
    #Go through all the namespaces in the datapack, make a list of linked
    #namespaces using the contents of prefix_linked_paths.txt in each namespace
    #The first entry in each inner list is the namespace with the links and
    #following entries are namespaces that are linked to
    #A dictionary is simultaneously created linking namespaces to its designated
    #variable prefix text string
    for ModulePath in ThisDataPath.iterdir():
        ModuleFnsPath = ModulePath / "functions"
        if ModuleFnsPath.exists():
            LinkedPathsFileName = ModuleFnsPath/"prefix_linked_paths.txt"
            if LinkedPathsFileName.is_file(): 
                LinkedPathsFile = LinkedPathsFileName.open()
                Prefix = LinkedPathsFile.readline().rstrip('\n')
                PrefixMap[ModulePath.name] = Prefix
                PathListEntry = [ModulePath.name]
                for NextPath in LinkedPathsFile:
                    CleanedPath = NextPath.strip()
                    if len(CleanedPath)>0:
                        PathListEntry.append(CleanedPath)
                PathList.append(PathListEntry)

    #Convert namespace links to prefixes
    for PathListEntry in PathList:            
        for i in range(1,len(PathListEntry)):
            DirName = PathListEntry[i]
            if (DirName in PrefixMap):
                PathListEntry[i] = PrefixMap[DirName]
            else:
                print("WARNING: Directory "+DirName+" linked to "+PathListEntry[0]+" either not present or not configured.")


    if bCreateOutput:
        #for each namespace, use it's corresponding linkage list as an input,
        #but first replace the namespace name with its designated prefix
        for ModulePath in ThisDataPath.iterdir():
            if ModulePath.is_dir():
                bConfiguredModule = False
                for PathListEntry in PathList:
                    DirName = PathListEntry[0]
                    if DirName==ModulePath.name:
                        bConfiguredModule = True
                        break
                        
                if bConfiguredModule:
                    file_parser.ResetObfuscationData()
                    
                    FunctionPath = ThisPackPath / "data" / DirName / "functions"
                
                    FileList = list(FunctionPath.glob('*.mcfunction'))
                    OutModPath = OutDataPath / DirName / "functions"
                    OutModPath.mkdir(parents=True,exist_ok=True)
                    for FilePath in FileList:
                        mcfunction_file = FilePath.open()
                        outFile = (OutModPath / FilePath.name).open('w')
                        PathListEntry[0] = PrefixMap[DirName]
                        if file_parser.ParseFunctionFile(mcfunction_file,outFile,PathListEntry)<0:
                            print("Parsing of file "+str(FilePath)+" failed!")
                        mcfunction_file.close()
                        outFile.close()
                else:
                    #Just copy the entire directory
                    shutil.copytree(str(ModulePath),str(OutDataPath / ModulePath.name))
            
    print("Finished!!!")
else:
    print("Apparently the current directory isn't a Minecraft datapack")

print("Press a key...")
msvcrt.getch()
