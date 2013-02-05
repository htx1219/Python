nums= file("QuickSort.txt").read()
nums = nums.split()
nums = [int(num) for num in nums]
nums.sort(reverse = True)
print nums[:10]
