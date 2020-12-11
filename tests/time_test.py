import sys
from statistics import mean

sys.path.insert(1, "./cogs/")

import op_score

# Test various wait times after clicking the match detail button
wait_time = [.45]
answer_list = ['5.5', '6.9', '8', '6.4', '6', '7.2', '7.7', '6.6', '8']

for i in wait_time:
    time_result = []
    passed = 0
    tests = 0
    for num in range(1):
        driver = op_score.driver_init("GoodMentalGamer")
        btn, requester, score_list, endTime = \
            op_score.get_score(driver)
        if btn == requester:
            passed += 1
        tests += 1
        time_result.append(endTime)
    print(f"For {i} second wait, the test took {mean(time_result)}.")
    print(f"{passed} out of {tests} tests passed.")
    print(f"Average score was {mean(score_list):.2f}.")
