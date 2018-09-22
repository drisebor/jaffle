execute at @e[tag=JAF_MCS] positioned ~-1 ~ ~1 run setblock ~ ~ ~ repeating_command_block[facing=up]{auto:1,Command:"function jaf_base:rotatedownsegment"}
execute at @e[tag=JAF_MCS] positioned ~-1 ~1 ~1 run setblock ~ ~ ~ chain_command_block[facing=up]{auto:1,Command:"execute unless entity @e[scores={JAF_LookDown=1..}] at @e[tag=JAF_MCS] positioned ~-1 ~ ~1 run fill ~ ~ ~ ~ ~1 ~ bedrock"}
