#create empty list
#create empty dictionary
#for every folder with path <datapack path>/data/<folder name>/functions
#   look for file which has extension followed by other folders referenced
#   add data to dictionary with folder name as key and extension as value
#   add following to list: ["folder name","other folder 1", "other folder 2"...]
#
#for every entry in list,
#   use the dictionary to find the extension for each of the other folders and replace folder name

#create output folder structure
#
#For each folder identified by folder name:
#   modify corresponding list entry, replacing folder name with extension
#   for each function file
#       run file_parser.ParseCommandFile
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

    for PathListEntry in PathList:            
        for i in range(1,len(PathListEntry)):
            DirName = PathListEntry[i]
            if (DirName in PrefixMap):
                PathListEntry[i] = PrefixMap[DirName]
            else:
                print("WARNING: Directory "+DirName+" linked to "+PathListEntry[0]+" either not present or not configured.")


    if bCreateOutput:
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
