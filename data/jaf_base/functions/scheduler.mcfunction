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

#keep track of clock ticks by incrementing a score
scoreboard players add @e[tag=JAF_MCS] JAF_OST 1
scoreboard players set @e[tag=JAF_MCS,scores={JAF_OST=20..}] JAF_OST 0

function jaf_base:everytick

#execute depending on the 50msec clock tick number
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=0}] run function jaf_base:tick0
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=1}] run function jaf_base:tick1
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=2}] run function jaf_base:tick2
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=3}] run function jaf_base:tick3
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=4}] run function jaf_base:tick4
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=5}] run function jaf_base:tick5
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=6}] run function jaf_base:tick6
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=7}] run function jaf_base:tick7
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=8}] run function jaf_base:tick8
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=9}] run function jaf_base:tick9
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=10}] run function jaf_base:tick10
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=11}] run function jaf_base:tick11
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=12}] run function jaf_base:tick12
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=13}] run function jaf_base:tick13
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=14}] run function jaf_base:tick14
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=15}] run function jaf_base:tick15
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=16}] run function jaf_base:tick16
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=17}] run function jaf_base:tick17
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=18}] run function jaf_base:tick18
execute if entity @e[tag=JAF_MCS,scores={JAF_OST=19}] run function jaf_base:tick19

