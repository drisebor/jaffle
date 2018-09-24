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

import re
import sys

stGetCmd=0
stAnyCmd=1

stScoreboardCmd=2
stTagCmd=3
stPlayersCmd=4
stObjectivesCmd=5
stTeamsCmd=6
stObjAtThree=7
stObjAtFive=8
stObjAtFiveEight=9
stSayCmd=10

NameDict = {}
CurrNameStr = "AAAAA"



LineNum = 1
ErrorData = []

def ResetObfuscationData():
    global NameDict
    global CurrNameStr
    NameDict = {}
    CurrNameStr = "AAAAA"
    return

def SetError(LocStr,Code):
    global LineNum
    ErrorData.append([LocStr,Code,LineNum])
    return Code*-1


def ReadOneChar(inFile):
    global LineNum
    char = inFile.read(1)
    if char=='\n': LineNum += 1
    return char


#tested B4 13/6/18
def IncrNameStr():
    global CurrNameStr
    LocalNameStr = CurrNameStr
    IncrFound = False
    CurrNameLen = len(LocalNameStr)
    CurrIndex = 0
    while not IncrFound:
        if LocalNameStr[CurrIndex]=='z':
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

    CurrNameStr = LocalNameStr
    return


def StartLine(CurrFile):
    char = ' '
    while char!='' and char in " \t\r\f\v\n":
        char = ReadOneChar(CurrFile)

    return char


def SkipComment(CurrFile):
    char = ' '
    while not (char=='\n' or char==''):
        char = ReadOneChar(CurrFile)
    return char


def GetNextNonWS(CurrFile,bIncludeNL=False):
    if bIncludeNL:
        CompText = " \t\r\f\v\n"
    else:
        CompText = " \t\r\f\v"
    char = ' '
    while (char in CompText) and (char!=''):
        char = ReadOneChar(CurrFile)
    return char


def WriteNextNonWS(myMC_File,outFile):
    char = GetNextNonWS(myMC_File)
    outFile.write(char)
    return char


def EndQuoteBS_Count(QuoteDepth):
    return (1<<(QuoteDepth-1)) - 1


def IncrBS_Count(BS_Count,QuoteDepth):
    BS_Count += 1
    if BS_Count>=(1<<QuoteDepth):
        BS_Count = 0
    return BS_Count


def ParseBlockData(myMC_File,outFile):
    outFile.write('[')
    while True:
        char = ReadOneChar(myMC_File)
        outFile.write(char)
        if char=='': return SetError("Block Data",0)
        elif char==']': return ord(char)


#Looks past whitespace followed by series of backspace followed by whitespace
#for the next character.
#Writes the character to output if it is a " (otherwise it might be
#a tag or scoreboard variable that needs obfuscating)
def SkipBS_WS(myMC_File,outFile):
    char = GetNextNonWS(myMC_File,True)
    #^Get the next non-whitespace char, skipping newlines as well
    while char=='\\':
        outFile.write(char)
        char = ReadOneChar(myMC_File)
    if char in " \t\r\f\v\n":
        outFile.write(' ')
        char = GetNextNonWS(myMC_File)
    if char=='"':
        outFile.write(char)
    return char


def ParseText(myMC_File,outFile,EndCharStr):
    char = GetNextNonWS(myMC_File)
    WhiteSpaceStr = ""
    while not (char in EndCharStr or char==''):
        if char in " \t\r\f\v\n":
            WhiteSpaceStr = WhiteSpaceStr + char
        else:
            if len(WhiteSpaceStr)>0:
                outFile.write(WhiteSpaceStr)
                WhiteSpaceStr = ""
            outFile.write(char)
        char = GetNextNonWS(myMC_File)
    return char
        

#Takes a list of score selectors. Looks for the closing }, then get the next char after
#which may legitimately be ',' or ']', writes this char to output and returns it.
#Tested 25/7/18
def ParseScoreSelectors(myMC_File,outFile,ModList):
    global CurrNameStr
    char = GetNextNonWS(myMC_File)
    outFile.write(char) #assume first char is '{'
    while True:
        #get score
        char = GetNextNonWS(myMC_File)
        if char=='': return SetError("Score Selectors",1)
        char = ParseVar(char,myMC_File,outFile,ModList)
##        ScoreText = ""
##        while (char >= '0' and char <='9') or \
##        (char >='A' and char <='Z') or (char>='a' and char <='z'):
##            ScoreText = ScoreText + char
##            char = ReadOneChar(myMC_File)
##
##        #Obfuscate the score
##        if not ScoreText in NameDict:
##            NameDict[ScoreText] = CurrNameStr
##            IncrNameStr()
##        outFile.write(ModList[0]+NameDict[ScoreText])

        if char in " \t\r\f\v\n":
            char = GetNextNonWS(myMC_File)

        if char!='=':
            return SetError("Score Selectors",2)

        outFile.write(char) #must be =

        #get the value
        char = GetNextNonWS(myMC_File)
        while not (char==',' or char=='}' or char==']' or char==''):
            outFile.write(char)
            char = GetNextNonWS(myMC_File)

        if char==',':
            outFile.write(char)
        if char==']':
            return SetError("Score Selectors",3)
        elif char=='':
            return SetError("Score Selectors",0)
        elif char=='}':
            outFile.write(char)
            return ord(char)


#Tested with ParseTagsList
#12/9/18 modified and retested
def ParseVar(StartChar,myMC_File,outFile,ModList):
    global CurrNameStr
    VarText = StartChar
    char = ReadOneChar(myMC_File)
    
    while (char=='_') or (char>='a' and char<='z') or \
          (char>='A' and char<='Z') or (char>='0' and char<='9'):
        VarText += char
        char = ReadOneChar(myMC_File)

    bModFound = False
    for ModText in ModList:
        if len(VarText)>=len(ModText):
            if VarText[0:len(ModText)]==ModText:
                bModFound = True
                break
    if bModFound:
        outFile.write(VarText)
        return char
    
    if not VarText in NameDict:
        NameDict[VarText] = CurrNameStr
        IncrNameStr()
    outFile.write(ModList[0]+NameDict[VarText])   

    return char


#processes the contents of a string literally. Just looks for the end of the string
#writes the final " to the file
#returns 0 if the end of the file is encountered,
#else if correct number of backspace encountered before ", returns "
#else returns -1 if there is not enough \ (shouldn't happen with correct command syntax)
#Tested 13/6/18
def ParseString(myMC_File,outFile,QuoteDepth):
    if QuoteDepth<1:
        return SetError("String",1) #just checking
    BS_Count = 0
    while True:
        char = ReadOneChar(myMC_File)
        outFile.write(char)
        if char=='\\':
            BS_Count = IncrBS_Count(BS_Count,QuoteDepth)
        elif char=='"':
            if BS_Count==EndQuoteBS_Count(QuoteDepth):
                return ord(char)
            elif BS_Count<EndQuoteBS_Count(QuoteDepth+1):
                return SetError("String",2) #this shouldn't happen with correct command syntax
            BS_Count = 0
        elif char=='':
            return SetError("String",0)
        else:
            BS_Count = 0


#Processes a JSON String. Tests for nested quotes but doesn't track the nesting level.
#The text in the string will not be checked for commands or variables.
#The end of the text is identified by the closing ".
#Doesn't change the text, but returns the string if it is a single token.
#The opening " will have already been processed
#Tested 25/7/2018
def ParseJSON_String(myMC_File,outFile,QuoteDepth):
#Returns the JSON string as a string only if there are only whitespace and alphanumeric characters.
#Otherwise returns the trailing "
#Returns empty string if an end of file is encountered.

    bReturnString = True
    BS_Count = 0
    JSON_String = ""
    while True:
        char = ReadOneChar(myMC_File)
        outFile.write(char)
        if char=='\\':
            BS_Count = IncrBS_Count(BS_Count,QuoteDepth)
        elif char=='"':
            if BS_Count==EndQuoteBS_Count(QuoteDepth):
                if bReturnString:
                    return JSON_String
                else:
                    return char
            elif BS_Count<EndQuoteBS_Count(QuoteDepth+1):
                return "" #this shouldn't happen with correct command syntax
            else:
                #Treat this as a literal ".
                BS_Count = 0
                bReturnString = False
        elif (char >= '0' and char <='9') or (char>='a' and char<='z') or (char>='A' and char<='Z'):
            BS_Count = 0
            JSON_String =JSON_String+char
        elif char=='':
            return ""
        else:
            BS_Count = 0
            bReturnString = False


#Tested 26/8/18
#Tested:
#no modifier and following whitespace,
#no modifier and no following char(eof)
#tag modifiers, scores modifier
#12/9/18 Retested and tested NBT data
def ParseSelector(myMC_File,outFile,ModList,QuoteDepth):
#Returns ord(']') or following char value if no modifier
#only prints the characters in the selector
    outFile.write('@')

    #get the entity type char
    char = ReadOneChar(myMC_File)
    if char>'z' or char<'a':
        return SetError("Selector",1)
    outFile.write(char)

    #is there a target selector?
    char = ReadOneChar(myMC_File)
    if char=='[':
        outFile.write(char)
    elif char=='':
        return SetError("Selector",0)
    else:
        return ord(char)

    while True:
        #Get argument
        char = GetNextNonWS(myMC_File)
        ArgText = ""
        while (char >= 'a' and char <='z') or char=='_':
            ArgText = ArgText + char
            outFile.write(char)
            char = ReadOneChar(myMC_File)

        if char in " \t\r\f\v":
            char = GetNextNonWS(myMC_File)

        if char=='':
            return SetError("Selector",2)
        elif not char=='=':
            return SetError("Selector",3)

        outFile.write(char) #must be '='

        #Get value
        if ArgText=="scores":
            ResChar = ParseScoreSelectors(myMC_File,outFile,ModList)
        elif ArgText=="tag":
            char = GetNextNonWS(myMC_File)
            if char=='!':
                outFile.write(char)
                char = GetNextNonWS(myMC_File)
            char = ParseVar(char,myMC_File,outFile,ModList)
            if char=='':
                return SetError("Selector",4)
            ResChar = ord(char)            
        elif ArgText=="nbt":
            char = GetNextNonWS(myMC_File)
            #char should always be '{'
            ResChar = ParseNBT_Data(myMC_File,outFile,ModList,QuoteDepth)
        else:
            char = ParseText(myMC_File,outFile,",]")
            if char=='': return SetError("Selector",5)
            ResChar = ord(char)
        if ResChar<0:
            return SetError("Selector",6)
        char = chr(ResChar)
        if char in " \t\r\f\v" or char=='}':
            char = GetNextNonWS(myMC_File)
        outFile.write(char)
        if char==']':
            return ord(char)
        elif not char==',':
            return SetError("Selector",7)


#Testing finished 27/8/18
#Tested objective string, name/selector string, backslashes, whitespace around commas
#Modified and tested on 12/9/18
def ParseJSON_Text(myMC_File,outFile,ModList,QuoteDepth):
    BS_Count = 0
    outFile.write('[')
    #^this is done here because we assume the presence of [ triggered call of
    #ParseJSON_Text
    DataLevel = 1
    while DataLevel>0:
        bGetSeparator = True
        bExpectCmd = False
        #Get the first char and check if [ or { or "

        #skip past any \ and whitespace to get first char indicating value type
        char = SkipBS_WS(myMC_File,outFile)
        if char=='"':
            JSON_String = ParseJSON_String(myMC_File,outFile,QuoteDepth+1)
            if len(JSON_String)==0:
                return SetError("JSON Text",1)
            char = GetNextNonWS(myMC_File)
            outFile.write(char)
            if char==':':
                char = SkipBS_WS(myMC_File,outFile)
                #^char should be opening " or { or [
                if JSON_String=="objective":
                    char = ParseVar(GetNextNonWS(myMC_File),myMC_File,outFile,ModList)
                    if char=='\\':
                        outFile.write(char)
                        char = SkipBS_WS(myMC_File,outFile)
                    if not char=='"':
                        return SetError("JSON Text",2) #char has to be " - the close quote.
                    outFile.write(char)
                    #Need to get separator char
                elif JSON_String=="selector" or JSON_String=="name":
                    char = GetNextNonWS(myMC_File)
                    if char=='@':
                        ResChar = ParseSelector(myMC_File,outFile,ModList,QuoteDepth+1)
                        if ResChar<=0:
                            return SetError("JSON Text",3)
                        char = chr(ResChar)
                        if char=='\\':
                            outFile.write(char)
                            char = SkipBS_WS(myMC_File,outFile)
                        elif char=='"':
                            outFile.write(char)
                        elif char==']' or char in " \t\r\f\v":
                            char = SkipBS_WS(myMC_File,outFile)
                        if char!='"':
                            return SetError("JSON Text",4)
                    else:
                        outFile.write(char)
                        ResVal = ParseString(myMC_File,outFile,QuoteDepth+1)
                        if ResVal<=0:
                            return SetError("JSON Text",5)
                    #Need to get separator char
                elif JSON_String=="action":
                    ActionString = ParseJSON_String(myMC_File,outFile,QuoteDepth+1)
                    if ActionString=="run_command":
                        bExpectCmd = True
                    else:
                        if len(ActionString)==0:
                            return SetError("JSON Text",6)
                        bExpectCmd = False
                    #Need to get separator char
                elif JSON_String=="value" and bExpectCmd:
                    ResChar = ParseCmd(myMC_File,outFile,ModList,QuoteDepth+1)
                    if ResChar<=0:
                        return SetError("JSON Text",7)
                    if not chr(ResChar)=='"':
                        return SetError("JSON Text",8)
                    #Need to get separator char
                else:
                    if char=='"':
                        ResVal = ParseString(myMC_File,outFile,QuoteDepth+1)
                        if ResVal<=0:
                            return SetError("JSON Text",9)
                        #Need to get separator char
                    elif char=='{':
                        outFile.write(char)
                        bGetSeparator = False
                    elif char=='[':
                        outFile.write(char)
                        DataLevel+=1
                        bGetSeparator = False
                    else:
                        return SetError("JSON Text",10)
            else:
                if char==']':
                    DataLevel -= 1
                    if DataLevel==0:
                        return True;
                elif char==',':
                    bGetSeparator = False
                #if char=='}': the next section will look for separators
                    
            while bGetSeparator:
                char = GetNextNonWS(myMC_File)
                outFile.write(char)
                if char==']':
                    DataLevel -= 1
                    if DataLevel==0:
                        break;
                elif char=='}':
                    bExpectCmd = False
                elif char==',':
                    break                   
                else:
                    return SetError("JSON Text",11)
 

        else:
            outFile.write(char)
            if char=='[':
                DataLevel += 1
            elif char==']':
                DataLevel -= 1
            elif not (char=='{' or char=='}'):
                print ("Bad char is '"+char+'"')
                return SetError("JSON Text",12)

    return True


#Tested 13/6/18
#Modified, tested 12/9/18
def ParseTagsList(myMC_File,outFile,ModList):
    char = SkipBS_WS(myMC_File,outFile)
    while True:
        #Always expecting new tag or end list here. Not expecting ','
        #char contains the first char of the tag or the leading ",
        #or the final ]
        if char==']':
            return char
        elif char=='"':
            char = ParseVar("",myMC_File,outFile,ModList)
            outFile.write(char)
            if char=='\\':
                char = SkipBS_WS(myMC_File,outFile)
            if char!='"':
                return ''
            char = WriteNextNonWS(myMC_File,outFile)
            #^ skip to the non-ws char after the closing "
            if char==',':
                char = SkipBS_WS(myMC_File,outFile)
        elif (char=='_') or (char>='a' and char<='z') or \
          (char>='A' and char<='Z'): #Note: digit not permitted as first char
            char = ParseVar(char,myMC_File,outFile,ModList)
            if char in " \t\r\f\v":
                char = WriteNextNonWS(myMC_File,outFile)
                #^ skip to the non-ws char after the closing "
            else:
                outFile.write(char)
            if char==',':
                char = SkipBS_WS(myMC_File,outFile)
            
        else:
            return ''


#Testing completed 1/9/18
#All tested except for embedded commands
#Retested  and tested embedded commands 12/9/18
def ParseNBT_Data(myMC_File,outFile,ModList,QuoteDepth):
    outFile.write('{')
    #^this is done here because we assume the presence of { triggered call of
    #ParseNBT_Data
    DataLevel = 1
    while DataLevel>0:
        #Get NBT Tag or Value

        #skip past any \ and whitespace to get first char indicating value type
        char = SkipBS_WS(myMC_File,outFile)

        if char=='"': #note that tags inside strings are ignored, ie copied without examining the tag string itself
            ResChar = ParseString(myMC_File,outFile,QuoteDepth+1)
            if ResChar<=0:
                return SetError("NBT Data",1)
        else:
            if char=='{':
                outFile.write(char)
                DataLevel += 1
            elif char=='}':
                outFile.write(char)
                DataLevel -= 1
            elif not (char=='[' or char==']' or char==','):
                #is a tag or a non string primitive value
                NBT_Tag = ""
                while True:
                    if char=='}':
                        outFile.write(char)
                        DataLevel -= 1
                        break
                    elif char in " \t\r\f\v\n":
                        char = GetNextNonWS(myMC_File)
                        if not (char==':' or char==','): #*very* lenient. still inside tag, so we allow a single space at a time
                            outFile.write(' ')
                            
                    if char==':':
                        outFile.write(char)

                        #Get Value
                        if NBT_Tag=="Command":
                            char = SkipBS_WS(myMC_File,outFile)
                            if char!='"':
                                return SetError("NBT Data",2)
                            
                            ResChar = ParseCommand(myMC_File,outFile,ModList,QuoteDepth+1)
                            #should return "
                            if ResChar!=ord('"'):
                                print("ResChar: "+str(ResChar))
                                return SetError("NBT Data",3)
                            outFile.write(char)
                        elif NBT_Tag=="Text1" or NBT_Tag=="Text2" or NBT_Tag=="Text3" or NBT_Tag=="Text4":
                            char1 = SkipBS_WS(myMC_File,outFile)
                            char2 = GetNextNonWS(myMC_File,outFile)
                            if not(char1=='"' and char2=='['):
                                return SetError("NBT Data",4)
                            
                            ResChar = ParseJSON_Text(myMC_File,outFile,ModList,QuoteDepth+1)
                        elif NBT_Tag=="Tags":
                            outFile.write(GetNextNonWS(myMC_File)) #assume the next char is [
                            char = ParseTagsList(myMC_File,outFile,ModList)
                            if char!=']': SetError("NBT Data",5)
                            ResChar = 1 #Just to flag all ok
                        else: #let the top of the outer loop handle it
                            ResChar = 1 #just to flag all ok
                            
                        if ResChar<=0:
                            return SetError("NBT Data",6)
                        break
                    elif char==',':
                        outFile.write(char)
                        break
                    elif char=='':
                        return SetError("NBT Data",0)
                    else: #still in tag. keep reading chars
                        NBT_Tag = NBT_Tag + char
                        outFile.write(char)
                        char = ReadOneChar(myMC_File)
            else: #is [ or ] or ,
                outFile.write(char)

    return ord(char)


#Tested with ParseCommand
def ParseCmdText(char,myMC_File,outFile):
    CmdText = char
    while char!='' and \
          (char=='^' or char=='~' or char=='_' or char=='%' or\
           (char>='a' and char<='z') or (char>='*' and char<='Z')):
        outFile.write(char)
        char = ReadOneChar(myMC_File)
        if char=='':
            return ''
        CmdText = CmdText+char
    return CmdText


#Tested with ParseCommand
def GetSayText(myMC_File,outFile,QuoteDepth):
    BS_Count = 0
    while True:
        char = ReadOneChar(myMC_File)
        outFile.write(char)
        if char=='\n' or char=='':
            return char


#Testing completed 12/9/18    
def ParseCommand(myMC_File,outFile,ModList,QuoteDepth):
    char = StartLine(myMC_File)
    ArgCount = 0
    BS_Count = 0
    CmdState = stGetCmd
    CmdText = ""
    while True:
        #Char has not been written.
        if char!='\\': BS_Count = 0

        if char=='':
            return 0
        elif char in "\n#":
            if CmdState==stGetCmd:
                if char=='#':
                    return ord('H')
                    #^Special character to identify potential file header
                else:
                    return ord('O')
                    #^Special character to represent empty line
            else:
                outFile.write('\n')
                return ord(char)
        elif char in " \t\r\f\v":
            outFile.write(' ')
            if (ArgCount==2 and (CmdState==stObjectivesCmd or \
                                 CmdState==stTagCmd)) or \
                (ArgCount==3 and (CmdState==stPlayersCmd or \
                                  CmdState==stObjAtFive or \
                                  CmdState==stObjAtFiveEight)) or \
                (ArgCount==6 and CmdState==stObjAtFiveEight):
                char = ParseVar("",myMC_File,outFile,ModList)
                if not char in " \t\r\f\v#\"\n":
                    return SetError("Command",1)
                ArgCount += 1
            elif CmdState==stSayCmd:
                char = GetNextNonWS(myMC_File)
                outFile.write(char)
                char = GetSayText(myMC_File,outFile,QuoteDepth)
                return ord(char)
                #the only time a valid command completes in one go.
                #The rest of the line after the command is literal.
            else:
                char = GetNextNonWS(myMC_File)
        elif char=='{':
            ResParse = ParseNBT_Data(myMC_File,outFile,ModList,QuoteDepth)
            #^ Normally anything in curly brackets is NBT data.
            if ResParse>0:
                char = ReadOneChar(myMC_File)
                if not char in " \t\r\f\v\n#": return SetError("Command",2)
            else:
                return SetError("Command",3)

        elif char=='[':
            ResParse = ParseJSON_Text(myMC_File,outFile,ModList,QuoteDepth)
                #^ This is JSON formatted text such as used in tellraw or title
                #JSON text in signs won't be encountered here.
            if ResParse>0:
                char = ReadOneChar(myMC_File)
                if not char in " \t\r\f\v\n#": SetError("Command",4)
            else:
                return SetError("Command",5)

        elif char=='@':
            ResParse = ParseSelector(myMC_File,outFile,ModList,QuoteDepth)
            if ResParse<0:
                return SetError("Command",6)
            elif ResParse==0:
                return 0
            elif ResParse==ord(']'):
                char = ReadOneChar(myMC_File)
            else:
                char = chr(ResParse)
            if not char in " \t\r\f\v#\n": return SetError("Command",7)

        elif char=='\\':
            while char=='\\':
                BS_Count = IncrBS_Count(BS_Count,QuoteDepth)
                outFile.write(char)
                char = ReadOneChar(myMC_File)
            if char in " \t\r\f\v":
                outFile.write(' ')
                char = GetNextNonWS(myMC_File)

        elif char=='"':
            if QuoteDepth<1: return SetError("Command",8)
            if BS_Count==EndQuoteBS_Count(QuoteDepth):
                return ord(char)
            elif BS_Count<EndQuoteBS_Count(QuoteDepth+1):
                print("Quote depth messed up. Backspace Count: "+str(BS_Count)+" Quote Depth: "+str(QuoteDepth))
                return SetError("Command",9)
            else:
                #handle basic string
                if (ParseJSON_String(myMC_File,outFile,QuoteDepth)==""):
                    return SetError("Command",10) #EOF encountered
                char = ReadOneChar(myMC_File)

        else:
            #Extract command or generic argument
            CmdText = ParseCmdText(char,myMC_File,outFile)
            if len(CmdText)==0:
                return 0
            char = CmdText[len(CmdText)-1]
            CmdText = CmdText[:len(CmdText)-1]
            if char in " \t\r\f\v":
                if CmdText=="run":
                    CmdState = stGetCmd
                    ArgCount = -1
                elif CmdText=="say":
                    CmdState = stSayCmd
                elif CmdState==stGetCmd:
                    if CmdText=="scoreboard":
                        CmdState = stScoreboardCmd
                    elif CmdText=="tag":
                        CmdState = stTagCmd
                    else:
                        CmdState = stAnyCmd

                elif CmdState==stScoreboardCmd and ArgCount==1:
                    if CmdText=="players":
                        CmdState = stPlayersCmd
                    elif CmdText=="objectives":
                        CmdState = stObjectivesCmd
                    else:
                        CmdState = stAnyCmd

                elif CmdState==stObjectivesCmd and ArgCount==2 and CmdText=="setdisplay":
                    CmdState = stObjAtFive

                elif CmdState==stPlayersCmd:
                    if ArgCount==2 and (CmdText=="list" or CmdText=="enable"):
                        CmdState = stAnyCmd #no objectives in cmd so don't care whats next
                    elif ArgCount==2 and CmdText=="operation":
                        CmdState = stObjAtFiveEight

                elif CmdState==stTagCmd:
                    if ArgCount==2 and CmdText=="list":
                        CmdState = stAnyCmd #We aren't expecting any more text for this cmd

            else:
                while True:
                    if char=='[':
                        if (ParseBlockData(myMC_File,outFile)<0): return SetError("Command",10)
                        char = ReadOneChar(myMC_File)
                    elif char=='{':
                        if (ParseNBT_Data(myMC_File,outFile,ModList,QuoteDepth)<0):
                            return SetError("Command",11)
                        char = ReadOneChar(myMC_File)
                    elif char in " \t\r\f\v\n#\"\\":
                        break
                    else:
                        return SetError("Command",12) 
        if not char in " \t\r\f\v":
            ArgCount += 1


def ProcessHeaderLine(myMC_File,outFile):
    outFile.write('#')
    char = ' '
    while char!='' and char!='\n':
        char = ReadOneChar(myMC_File)
        outFile.write(char)
    return char


#Tested 12/9/18
def ParseFunctionFile(myMC_File,outFile,ModList):
    global ErrorData
    global LineNum
    ErrorData = []
    LineNum = 1
    bCommentHeader = True
    while True:
        ResChar = ParseCommand(myMC_File,outFile,ModList,0)
        if bCommentHeader:
            if ResChar==ord('H'):
                if (ProcessHeaderLine(myMC_File,outFile)==''):
                    return 0
            elif ResChar!=ord('O'):
                bCommentHeader = False
        elif ResChar==ord('H'):
            ResChar = ord('#') #its just a normal comment
            
        if ResChar==ord('#'):
            char = SkipComment(myMC_File)
            if char=='':
                return 0
        elif ResChar==0:
            return 0
        elif not (ResChar==ord('\n') or ResChar==ord('H') or ResChar==ord('O')):
            if ResChar<0:
                print("Error at line "+str(ErrorData[0][2]))
                for Error in ErrorData:
                    print("Failure in "+Error[0]+", Code: "+str(Error[1]))
                return -1
            else:
                print("Unknown parse result: "+str(ResChar))
                return -2





