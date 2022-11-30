
# Discrete moves
moves_discrete_dict={
    "no_move & no_attack":0,
    "left":1,
    "left_jump":2,
    "jump":3,
    "right_jump":4,
    "right":5,
    "right_down":6,
    "down":7,
    "left_down":8,
    "low_punch":9,
    "medium_punch":10,
    "high_punch":11,
    "low_kick":12,
    "medium_kick":13,
    "high_kick ":14,
    "low_punch & low_kick":15, #Buttons Combination
    "medium_punch & medium_kick":16, #Buttons Combination
    "high_punch & high_kick":17, #Buttons Combination
    }

# Multi-Discrete moves
moves_multi_dict={
    "no_move & no_attack":[0,0],
    "no_move & low_punch":[0,1],
    "no_move & medium_punch":[0,2],
    "no_move & high_punch":[0,3],
    "no_move & low_kick":[0,4],
    "no_move & medium_kick":[0,5],
    "no_move & high_kick":[0,6],
    "no_move & low_punch & low_kick":[0,7], #Buttons Combination
    "no_move & medium_punch & medium_kick":[0,8], #Buttons Combination
    "no_move & high_punch & high_kick":[0,9], #Buttons Combination
    }
