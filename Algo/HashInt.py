nums= file("HashInt1.txt").read()
nums = nums.split()
nums = [(int(num),1) for num in nums]
nums = dict(nums)
print len(nums)

goal = [231552,234756,596873,648219,726312,981237,988331,1277361,1283379]

def find_goal(i):
    for j in nums.keys():
        if i-j in nums:
            return True
    return False
            
for i in goal:
    print int(find_goal(i))
