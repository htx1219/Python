nums= file("QuickSort.txt").read()
nums = nums.split()
nums = [int(num) for num in nums]
def quicksort1(nums,s=0,e=10000, t=[]):
    if e-s<=1:
        return
    else:
        p = nums[s]
        t += [0]*(e-s-1)
        i = s+1
        for j in range(s+1,e):
            if nums[j]<p:
                nums[i], nums[j]=nums[j], nums[i]
                i += 1
        nums[s], nums[i-1] = nums[i-1], p
        #print nums, s,i,e, len(t)
        quicksort1(nums, s, i-1,t)
        quicksort1(nums, i, e,t)
    return len(t)
            
def quicksort2(nums,s=0,e=10000, t=[]):
    if e-s<=1:
        return
    else:
        p = nums[e-1]
        nums[s],nums[e-1] = p, nums[s]
        t += [0]*(e-s-1)
        i = s+1
        for j in range(s+1,e):
            if nums[j]<p:
                nums[i], nums[j]=nums[j], nums[i]
                i += 1
        nums[s], nums[i-1] = nums[i-1], p
        #print nums, s,i,e, len(t)
        quicksort2(nums, s, i-1,t)
        quicksort2(nums, i, e,t)
    return len(t)

def choose_med(nums, s, e):
    b=s+(e-s+1)/2-1
    if nums[b]<nums[e-1]:
        if nums[b]> nums[s]:
            pivot = b
        elif nums[e-1]<nums[s]:
            pivot = e-1
        else:
            pivot = s
    else:
        if nums[e-1]> nums[s]:
            pivot = e-1
        elif nums[b]<nums[s]:
            pivot = b
        else:
            pivot = s
    #print nums[s], nums[b], nums[e-1]
    #print b, nums[pivot]
    return pivot

def quicksort3(nums,s=0,e=10000, t=[]):
    if e-s<=1:
        return
    else:
        pivot = choose_med(nums, s, e)
        p = nums[pivot]
        nums[s],nums[pivot] = p, nums[s]
        t += [0]*(e-s-1)
        i = s+1
        for j in range(s+1,e):
            if nums[j]<p:
                nums[i], nums[j]=nums[j], nums[i]
                i += 1
        nums[s], nums[i-1] = nums[i-1], p
        #print nums, s,i,e, len(t)
        #print nums[s:e], p
        quicksort3(nums, s, i-1,t)
        quicksort3(nums, i, e,t)
    return len(t)
