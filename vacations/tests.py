from django.test import TestCase

# Create your tests here.


big_result1 = list()
big_result2 = list()

data = 0
test_result = {"2" : data}

#
# print("big_result:::", big_result)  # {"2" : 0}
#
#
# test_result["2"] = 1
# big_result.append(test_result)
#
# print("big_result1:::", big_result) # {"2" : 1}
#
#
# test_result["2"] = 2
# big_result.append(test_result)
#
# print("big_result2:::", big_result) # {"2" : 2}, {"2" : 2}

# 변수를 다르게 설정해서 얻어낸 결과. Q. 그렇다면 동일한 변수를 가지고 동일한 결과를 찾는 방법을 연구해볼 것
for i in range(3):
    globals()["key{}".format(i)] = {"2" : i }
    big_result1.append(globals()["key{}".format(i)])

print("big_result1_for::::", big_result1)

# Q. 그렇다면 동일한 변수를 가지고 동일한 결과를 찾는 방법을 연구해볼 것 // 그치만 불가능. 왜냐면 slack에서 지정한 key값을 넘겨줘야 하기 때문에.
for i in range(3):
    test_result = {f"{i}" : i}
    big_result2.append(test_result)

print("big_result2_for::::", big_result2)

