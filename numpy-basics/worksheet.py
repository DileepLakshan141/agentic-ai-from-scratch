import numpy as np

# normal array
np_arr = np.array([1, 2, 3, 4, 5])

# array with values start end interval
arranged = np.arange(0, 20 + 1, 2)

# array with zeros
zeros = np.zeros(10)

# identity matrix 3x3
identity = np.eye(3)

# random (floating point vals)
random = np.random.rand(5)

# random ints 0 to 10
random2 = np.random.randint(0, 10, size=10)

# multi dimensions array

# essential props
# .shape .dtype .ndim .size

# 2d = rows x cols
# 3d = page x rows x cols

print(random2)
