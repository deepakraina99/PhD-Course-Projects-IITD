@echo off
setlocal ENABLEDELAYEDEXPANSION

if not exist ".\testLogs\" md ".\testLogs\"
if not exist "testLogs\part1\" md "testLogs\part1\"
if not exist "testLogs\part2\" md "testLogs\part2\"
if not exist "testLogs\part3\" md "testLogs\part3\"
if not exist "testLogs\part4\" md "testLogs\part4\"
if not exist "testLogs\part5\" md "testLogs\part5\"

rem rem TEST 1, check action and change state
rem python planner.py  --world .\jsons\home_worlds\world_home0.json --goal .\jsons\home_goals\goal0.json --input part1 > "testLogs\part1\output.txt"

rem rem TEST 2, check plan in world 0 forward
rem python planner.py  --world .\jsons\home_worlds\world_home0.json --goal .\jsons\home_goals\goal0.json --input part2 > "testLogs\part2\output_G0_W0.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home0.json --goal .\jsons\home_goals\goal1.json --input part2 > "testLogs\part2\output_G1_W0.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home0.json --goal .\jsons\home_goals\goal2.json --input part2 > "testLogs\part2\output_G2_W0.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home0.json --goal .\jsons\home_goals\goal3.json --input part2 > "testLogs\part2\output_G3_W0.txt"

rem rem TEST 3, check plan in world 0 backward
rem python planner.py  --world .\jsons\home_worlds\world_home0.json --goal .\jsons\home_goals\goal0.json --input part3 > "testLogs\part3\output_G0_W0.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home0.json --goal .\jsons\home_goals\goal1.json --input part3 > "testLogs\part3\output_G1_W0.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home0.json --goal .\jsons\home_goals\goal2.json --input part3 > "testLogs\part3\output_G2_W0.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home0.json --goal .\jsons\home_goals\goal3.json --input part3 > "testLogs\part3\output_G3_W0.txt"

rem rem TEST 4, check accelerated planning in all goals 
rem python planner.py  --world .\jsons\home_worlds\world_home0.json --goal .\jsons\home_goals\goal0.json --input part4 > "testLogs\part4\output_G0_W0.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home0.json --goal .\jsons\home_goals\goal1.json --input part4 > "testLogs\part4\output_G1_W0.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home0.json --goal .\jsons\home_goals\goal2.json --input part4 > "testLogs\part4\output_G2_W0.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home0.json --goal .\jsons\home_goals\goal3.json --input part4 > "testLogs\part4\output_G3_W0.txt"

rem rem TEST 5, check accelerated planning in all goals and all worlds
rem python planner.py  --world .\jsons\home_worlds\world_home1.json --goal .\jsons\home_goals\goal0.json --input part5 > "testLogs\part5\output_G0_W1.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home1.json --goal .\jsons\home_goals\goal1.json --input part5 > "testLogs\part5\output_G1_W1.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home1.json --goal .\jsons\home_goals\goal2.json --input part5 > "testLogs\part5\output_G2_W1.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home1.json --goal .\jsons\home_goals\goal3.json --input part5 > "testLogs\part5\output_G3_W1.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home0.json --goal .\jsons\home_goals\goal4.json --input part5 > "testLogs\part5\output_G4_W0.txt"

rem python planner.py  --world .\jsons\home_worlds\world_home2.json --goal .\jsons\home_goals\goal0.json --input part5 > "testLogs\part5\output_G0_W2.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home2.json --goal .\jsons\home_goals\goal1.json --input part5 > "testLogs\part5\output_G1_W2.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home2.json --goal .\jsons\home_goals\goal2.json --input part5 > "testLogs\part5\output_G2_W2.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home2.json --goal .\jsons\home_goals\goal3.json --input part5 > "testLogs\part5\output_G3_W2.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home1.json --goal .\jsons\home_goals\goal4.json --input part5 > "testLogs\part5\output_G4_W1.txt"

rem python planner.py  --world .\jsons\home_worlds\world_home3.json --goal .\jsons\home_goals\goal0.json --input part5 > "testLogs\part5\output_G0_W3.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home3.json --goal .\jsons\home_goals\goal1.json --input part5 > "testLogs\part5\output_G1_W3.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home3.json --goal .\jsons\home_goals\goal2.json --input part5 > "testLogs\part5\output_G2_W3.txt"
python planner.py  --world .\jsons\home_worlds\world_home3.json --goal .\jsons\home_goals\goal3.json --input part5 > "testLogs\part5\output_G3_W3.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home2.json --goal .\jsons\home_goals\goal4.json --input part5 > "testLogs\part5\output_G4_W2.txt"

rem python planner.py  --world .\jsons\home_worlds\world_home4.json --goal .\jsons\home_goals\goal0.json --input part5 > "testLogs\part5\output_G0_W4.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home4.json --goal .\jsons\home_goals\goal1.json --input part5 > "testLogs\part5\output_G1_W4.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home4.json --goal .\jsons\home_goals\goal2.json --input part5 > "testLogs\part5\output_G2_W4.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home4.json --goal .\jsons\home_goals\goal3.json --input part5 > "testLogs\part5\output_G3_W4.txt"
rem python planner.py  --world .\jsons\home_worlds\world_home3.json --goal .\jsons\home_goals\goal4.json --input part5 > "testLogs\part5\output_G4_W3.txt"
