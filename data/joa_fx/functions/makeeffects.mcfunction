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

scoreboard players set @e[scores={JOA_FX_Num=1}] JOA_AC_Timer 0
scoreboard players set @e[scores={JOA_FX_Num=1}] JOA_FX_Num 0
#^set to zero means this function will still execute but won't reset the timer
data merge entity @e[scores={JOA_AC_Timer=0},limit=1] {NoAI:1}
execute as @e[scores={JOA_AC_Timer=2..}] at @s run teleport @s ~ ~0.1 ~ ~15 ~
execute as @e[scores={JOA_AC_Timer=0..}] at @s run particle minecraft:entity_effect ^1 ^1 ^0.5 0.2 0.2 0.2 1 5

execute at @e[scores={JOA_AC_Timer=0}] run playsound minecraft:block.note.chime master @a ~ ~ ~ 5.0
execute at @e[scores={JOA_AC_Timer=2}] run playsound minecraft:block.note.chime master @a ~ ~ ~ 5.0 1.0595
execute at @e[scores={JOA_AC_Timer=4}] run playsound minecraft:block.note.chime master @a ~ ~ ~ 5.0 1.1225
execute at @e[scores={JOA_AC_Timer=6}] run playsound minecraft:block.note.chime master @a ~ ~ ~ 5.0 1.1892
execute at @e[scores={JOA_AC_Timer=8}] run playsound minecraft:block.note.chime master @a ~ ~ ~ 5.0 1.2599
execute at @e[scores={JOA_AC_Timer=10}] run playsound minecraft:block.note.chime master @a ~ ~ ~ 5.0 1.3348
execute at @e[scores={JOA_AC_Timer=12}] run playsound minecraft:block.note.chime master @a ~ ~ ~ 5.0 1.4142
execute at @e[scores={JOA_AC_Timer=14}] run playsound minecraft:block.note.chime master @a ~ ~ ~ 5.0 1.4983
execute at @e[scores={JOA_AC_Timer=16}] run playsound minecraft:block.note.chime master @a ~ ~ ~ 5.0 1.5874
execute at @e[scores={JOA_AC_Timer=18}] run playsound minecraft:block.note.chime master @a ~ ~ ~ 5.0 1.6818
execute at @e[scores={JOA_AC_Timer=20}] run playsound minecraft:block.note.chime master @a ~ ~ ~ 5.0 1.7818
execute at @e[scores={JOA_AC_Timer=22}] run playsound minecraft:block.note.chime master @a ~ ~ ~ 5.0 1.8877
execute at @e[scores={JOA_AC_Timer=24}] run playsound minecraft:block.note.chime master @a ~ ~ ~ 5.0 2.0000

data merge entity @e[scores={JOA_AC_Timer=24},limit=1] {NoAI:0}

scoreboard players reset @e[scores={JOA_AC_Timer=24..}] JOA_FX_Num
scoreboard players reset @e[scores={JOA_AC_Timer=24..}] JOA_AC_Timer

scoreboard players add @e[scores={JOA_AC_Timer=..24}] JOA_AC_Timer 1
