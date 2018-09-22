execute as @e[scores={JAF_TurnLeft=1..}] at @s run tp @s ~ ~ ~ ~-10 ~
scoreboard players remove @e[scores={JAF_TurnLeft=1..}] JAF_TurnLeft 1
scoreboard players reset @e[scores={JAF_TurnLeft=0}] JAF_TurnLeft
