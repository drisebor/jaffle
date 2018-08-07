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

#executes on Tick 2
scoreboard players add @e[tag=JAF_MCS] JAF_FiveMinTimer 1
scoreboard players set @e[tag=JAF_MCS,scores={JAF_FiveMinTimer=300..}] JAF_FiveMinTimer 0

#Check for a five second timeout
scoreboard players operation @e[tag=JAF_MCS] JAF_DivRem = @e[tag=JAF_MCS] JAF_FiveMinTimer
scoreboard players operation @e[tag=JAF_MCS] JAF_DivRem %= @e[tag=JAF_MCS] JAF_ConstFive
execute if entity @e[tag=JAF_MCS,scores={JAF_DivRem=0}] run function jaf_base:fivesecprocess

#Check for a one minute timeout
scoreboard players operation @e[tag=JAF_MCS] JAF_DivRem2 = @e[tag=JAF_MCS] JAF_FiveMinTimer
scoreboard players operation @e[tag=JAF_MCS] JAF_DivRem2 %= @e[tag=JAF_MCS] JAF_ConstSixty
execute if entity @e[tag=JAF_MCS,scores={JAF_DivRem2=0}] run function jaf_base:oneminprocess

#Check for a five minute timeout
execute if entity @e[tag=JAF_MCS,scores={JAF_FiveMinTimer=0}] run function jaf_base:fiveminprocess

function jaf_mod0:tick2
function jaf_mod1:tick2
function jaf_mod2:tick2
function jaf_mod3:tick2
function jaf_mod4:tick2
function jaf_mod5:tick2
function jaf_mod6:tick2
function jaf_mod7:tick2
function jaf_mod8:tick2
function jaf_mod9:tick2
