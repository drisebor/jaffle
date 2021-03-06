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

#This function is intended to be run by a player command while in the game.
#It forces Jaffle to reinstall itself

tag @s add JAF_Resetting
summon armor_stand ~ ~ ~ {Tags:[JAF_TempPosition]}
tp @e[tag=JAF_TempPosition] @s

execute at @e[tag=JAF_MCS] run tp @s ~ ~255 ~
execute at @e[tag=JAF_MCS] run fill ~-3 0 ~-3 ~3 4 ~3 bedrock
execute at @e[tag=JAF_MCS] run kill @e[type=armor_stand,distance=..0.1]
function jaf_base:setup
tp @s @e[tag=JAF_TempPosition,limit=1]
kill @e[tag=JAF_TempPosition]
tag @s remove JAF_Resetting
