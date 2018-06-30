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

title @a subtitle [{"text":"Jaffle powered!","color":"gold"}]
function jaf_pack:title
scoreboard objectives add JAF_TitleTimer dummy
scoreboard players set @e[tag=JAF_MCS] TitleTimer 0
execute at @e[tag=JAF_MCS] positioned ~1 ~ ~ run setblock ~ ~ ~ repeating_command_block[facing=up]{auto:1,Command:"scoreboard players add @e[tag=JAF_MCS] JAF_TitleTimer 1"}
execute at @e[tag=JAF_MCS] positioned ~1 ~1 ~ run setblock ~ ~ ~ chain_command_block[facing=up]{auto:1,Command:"execute if entity @e[scores={JAF_TitleTimer=140..}] run function jaf_base:info"}

