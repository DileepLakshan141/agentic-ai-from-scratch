import numpy as np

a = np.array([1, 2, 3, 4])
b = np.array([2, 4, 6, 8])

print("addition: ", a + b)
print("multiply: ", a * b)
print("subtract: ", a - b)
print("divide: ", a / b)

# note: comparison operation will perform that for each element in array

print("greater than: ", a >= b)

# manipulation
nums = np.arange(12)

print(nums)

# reshaping
reshaped = nums.reshape(3, 4)

print(reshaped)

# flatten
flattened = reshaped.flatten()

print(flattened)

# automatic reshaping use -1
reshaped = nums.reshape(4, -1)
print(reshaped)

# transposed
print(reshaped.transpose())

# vertical concat
a = [[1, 2], [2, 5]]
b = [[3, 5], [6, 9]]

print(np.vstack((a, b)))

print(np.hstack((a, b)))

print(np.concatenate((a, b), axis=0))
print(np.concatenate((a, b), axis=1))

# dimensions and axis deep
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(matrix)

sum_axis_0 = np.sum(matrix, axis=0)
sum_axis_1 = np.sum(matrix, axis=1)
print(sum_axis_0)
print(sum_axis_1)

# 3D -> depth, rows, cols so axis = 0 is depth 1 = rows , 2 = cols
