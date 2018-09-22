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

say performing Jaffle setup!

execute at @p align xz positioned ~0.5 ~ ~0.5 run summon armor_stand ~ 1 ~ {Tags:["JAF_MCS"],Invulnerable:1}
#^JAF_MCS = Jaffle (command mod platform) Mod Control Stand

execute at @e[tag=JAF_MCS] run setworldspawn ~ ~ ~
execute at @e[tag=JAF_MCS] run fill ~-3 0 ~-3 ~3 4 ~3 bedrock
execute at @e[tag=JAF_MCS] run fill ~ 1 ~ ~ 3 ~ air
execute at @e[tag=JAF_MCS] run fill ~-1 253 ~-1 ~1 255 ~1 barrier
execute at @e[tag=JAF_MCS] run setblock ~ 254 ~ daylight_detector

scoreboard objectives add JAF_OST dummy
#^JAF_OST = Joacomp One Second Timer
scoreboard objectives add JAF_FiveMinTimer dummy
scoreboard objectives add JAF_DivRem dummy
scoreboard objectives add JAF_DivRem2 dummy
#^This is required to to apparently a MC glitch
scoreboard objectives add JAF_ConstFive dummy
scoreboard objectives add JAF_ConstSixty dummy
scoreboard objectives add JAF_PlayerCount dummy
scoreboard objectives add JAF_RandomVal dummy
scoreboard objectives add JAF_TurnLeft dummy
scoreboard objectives add JAF_TurnRight dummy
scoreboard objectives add JAF_LookDown dummy
scoreboard players set @e[tag=JAF_MCS] JAF_PlayerCount 0
scoreboard players set @e[tag=JAF_MCS] JAF_ConstFive 5
scoreboard players set @e[tag=JAF_MCS] JAF_ConstSixty 60

function jaf_base:placerandomstands
scoreboard players set @e[tag=JAF_MCS] JAF_RandomVal 0
execute at @e[tag=JAF_MCS] run setblock ~ ~ ~ minecraft:repeating_command_block["facing"=up]{auto:1,Command:"function jaf_base:genrandomoptions"}
