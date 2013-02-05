nums= file("IntegerArray.txt").read()
nums = nums.split()
nums = [int(num) for num in nums]
def countinversion(nums):
    if len(nums)<=1:
        return 0
    q = len(nums)/2
    l = nums[:q]
    r = nums[q:]
    count = countinversion(l)+countinversion(r)
    i = j = 0
    l = l+["MAX"]
    r = r+["MAX"]
    for k in range(len(nums)):
        if l[i]<r[j]:
            nums[k] = l[i]
            i = i+1
        else:
            nums[k] = r[j]
            j = j+1
            count += len(l)-i-1
    return count
            
    
