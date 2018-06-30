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

DEBUG_LVL=0

def IncrNameStr():
    LocalNameStr = CurrNameStr[0]
    IncrFound = False
    CurrNameLen = len(LocalNameStr)
    CurrIndex = 0
    while not IncrFound:
        if LocalNameStr[CurrIndex]=='z':
            LocalNameStr= LocalNameStr[:CurrIndex]+\
                              'A'+\
                              LocalNameStr[CurrIndex+1:]
            CurrIndex+=1
            if CurrIndex>=len(LocalNameStr):
                LocalNameStr = LocalNameStr + "A"
                IncrFound = True
        else:
            IncrFound = True
            if LocalNameStr[CurrIndex]=='Z':
                LocalNameStr= LocalNameStr[:CurrIndex]+\
                              'a'+\
                              LocalNameStr[CurrIndex+1:]
            else:
                LocalNameStr= LocalNameStr[:CurrIndex]+\
                              chr(ord(LocalNameStr[CurrIndex])+1)+\
                              LocalNameStr[CurrIndex+1:]
                
    CurrNameStr[0] = LocalNameStr
    return

from pathlib import Path
import shutil
import msvcrt

ThisPackPath = Path().resolve()
DataPacksPath = ThisPackPath.parent
ModuleListFile = (ThisPackPath/"parse_modules.txt").open()
OutPackStr = ModuleListFile.readline().strip()
OutPackPath = DataPacksPath / OutPackStr
if OutPackPath.exists():
    print("The target path "+str(OutPackPath)+" already exists. Checking variables only...")
    bCreateOutput = False
else:
    bCreateOutput = True
    OutDataPath = OutPackPath / "data"
    OutDataPath.mkdir(parents=True,exist_ok=True)
    shutil.copy(str(ThisPackPath / "pack.mcmeta"),str(OutPackPath))
    shutil.copy(str(ThisPackPath / "LICENSE"),str(OutPackPath))

ModuleList = []
for Module in ModuleListFile: ModuleList.append(Module.strip())
ModuleListFile.close()
print("Modules: "+ str(ModuleList))
ThisDataPath = ThisPackPath / "data"
GlobalVarList = []
for ModulePath in ThisDataPath.iterdir():
    if ModulePath.is_dir():
        if str(ModulePath.name) in ModuleList:
            CurrNameStr = ["AA"]
            ModuleFnsPath = ModulePath / "functions"
            if DEBUG_LVL>0: print(str(ModuleFnsPath/"parse_data.txt\n====================================="))

            var_list = (ModuleFnsPath/"parse_data.txt").open()
            Prefix = var_list.readline().strip()

            #get all the variables to be obfuscated
            NameList = []
            for nextvar in var_list:
                nextvar = nextvar.strip()
                if len(nextvar)>0:
                    if nextvar in NameList:
                        if DEBUG_LVL>0: print("Variable "+nextvar+" is repeated in the parse data file")
                    else:
                        NameList.append(nextvar)
                        if nextvar in GlobalVarList:
                            print ("Variable name "+nextvar+" is used in multiple modules. Be careful of conflicts when testing development versions.")
                        else:
                            GlobalVarList.append(nextvar)
            var_list.close()

            if DEBUG_LVL>0: print("Original Name List Length: "+str(len(NameList)))
            #move vars that are subsets of other vars (in terms of var name) to later in the list
            i = 0
            while i < len(NameList):
                CheckName = NameList[i]
                j=len(NameList)-1
                while j>i:
                    OtherName = NameList[j]
                    if CheckName in OtherName:
                        if DEBUG_LVL>0: print("Moving "+CheckName+" to after "+OtherName)
                        nada = NameList.pop(i)
                        NameList.insert(j,CheckName)
                        break
                    
                    j-=1
                          
                if j==i:i+=1

            if DEBUG_LVL>0:
                print("Sorted Name List:\n----------------")
                print("Length: "+str(len(NameList)))
            
                for Name in NameList: print(Name)
                
            #generate obfuscated names
            NameDict = {}
            for nextvar in NameList:
                NameDict[nextvar] = CurrNameStr[0]
                IncrNameStr()

            if DEBUG_LVL>1:
                for Var,Obf in NameDict.items():
                    print(Var+": "+Obf)

            if bCreateOutput:
                #Generate the output module
                file_list = list(ModuleFnsPath.glob('*.mcfunction'))
                OutModPath = OutDataPath / ModulePath.name / "functions"
                OutModPath.mkdir(parents=True,exist_ok=True)
                for file_path in file_list:
                    mcfunction_file = file_path.open()
                    outFile = (OutModPath / file_path.name).open('w')

                    #Copy the license
                    Line = mcfunction_file.readline()
                    while len(Line)>0 and Line[0]=='#':
                        outFile.write(Line)
                        Line = mcfunction_file.readline()

                    #parse the function text    
                    while len(Line)>0:
                        cmd = Line.rsplit("#",1)[0].strip()
                        if len(cmd)>1:
                            for var in NameDict:
                                cmd = cmd.replace(var,Prefix+NameDict[var])
                            outFile.write(cmd+"\n")
                        Line = mcfunction_file.readline()                        

                    outFile.close()
                    mcfunction_file.close()

        elif bCreateOutput:
#            shutil.rmtree(str(OutDataPath / ModulePath.name),ignore_errors=True)
#^rmtree is a bit dangerous to use on the general public
            shutil.copytree(str(ModulePath),str(OutDataPath / ModulePath.name))

print("Finished!!")
print("Press a key...")
msvcrt.getch()

