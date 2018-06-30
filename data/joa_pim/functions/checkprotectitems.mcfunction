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

#executes every clock  tick

tag @e[tag=!Processed,type=item] add Check
execute if entity @e[tag=Check] run function joa_pim:findprotectitems
execute if entity @e[tag=SetupProtect] run function joa_pim:protectitems

execute at @e[tag=BlastOut] run execute as @e[tag=BlastOut] run tp ~ 0 ~

tag @e[tag=Protect,nbt={OnGround:0b},tag=!BlastedOut,tag=!BlastOut,tag=!WontFall,limit=1] add CheckFall
execute if entity @e[tag=CheckFall] run function joa_pim:checkfall
