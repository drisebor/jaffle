execute as @e[scores={JAF_LookDown=1..}] at @s run tp @s ~ ~ ~ ~ ~1
scoreboard players remove @e[scores={JAF_LookDown=1..}] JAF_LookDown 1
scoreboard players reset @e[scores={JAF_LookDown=0}] JAF_LookDown
