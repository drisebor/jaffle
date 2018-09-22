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

function jaf_pack:intro
function jaf_mod0:intro
function jaf_mod1:intro
function jaf_mod2:intro
function jaf_mod3:intro
function jaf_mod4:intro
function jaf_mod5:intro
function jaf_mod6:intro
function jaf_mod7:intro
function jaf_mod8:intro
function jaf_mod9:intro

tellraw @a [{"text":"\nJaffle version 1.3"}]
tellraw @a [{"text":"for more information about the Jaffle command mod platform go to "},{"text":"joacomp.com","color":"blue","clickEvent":{"action":"open_url","value":"https://joacomp.com/jaffle-minecraft-modding-platform"}},{"text":"\n\n"}]

#Finally remove the stuff that called this function
scoreboard objectives remove JAF_TitleTimer
execute at @e[tag=JAF_MCS] run fill ~1 ~ ~ ~1 ~1 ~ bedrock
