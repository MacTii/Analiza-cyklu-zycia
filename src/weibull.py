import pandas as pd
from math import log
import matplotlib.pyplot as plt
import numpy as np

filename = "Data_for_analysis.xlsx"

data = pd.read_excel(filename, skiprows=2)
data_sorted = data[["Time to failure", "Action"]].sort_values(
    by="Time to failure", ignore_index=True
)

# print(data_sorted) #printing an array with the Action and Time columns
# print(len(data_sorted))

rows = len(data_sorted)  # 196
# print(rows)

reverse_rank_r = []
for i in range(rows, 0, -1):
    reverse_rank_r.append(i)
    # print(i)

# print(reverse_rank_r) #printing an array with the Reverse rank r column
# print(len(reverse_rank_r))

estimate_of_survival_S = []
#estimate_of_survival_S.append(1)  # S(0) = 1
last_element = 1
for i in range(rows):
    if data_sorted["Action"][i] == "S":
        estimate_of_survival_S.append(None)
        continue
    else:
        value = last_element * reverse_rank_r[i] / (reverse_rank_r[i] + 1)
        last_element = value
        estimate_of_survival_S.append(value)

#estimate_of_survival_S.pop(0)  # delete 1 from list (S(0) = 1)

# print(estimate_of_survival_S) #printing an array with the Estimate of survival S column
# print(len(estimate_of_survival_S))

plotting_position = []
for i in range(rows):
    if data_sorted["Action"][i] == "S":
        plotting_position.append(None)
    else:
        plotting_position.append(log(-log(estimate_of_survival_S[i])))

# print(plotting_position) #printing an array with the log(-log(S)) column

plotting_position_time = []
for i in range(rows):
    if data_sorted["Action"][i] == "S":
        plotting_position_time.append(None)
    else:
        value = log(data_sorted["Time to failure"][i])
        plotting_position_time.append(value)

# print(plotting_position_time) #printing an array with the log(Time) column

x = []
y = []
for i in range(rows):
    if plotting_position_time[i] != None and plotting_position[i] != None:
        x.append(plotting_position_time[i])
        y.append(plotting_position[i])

# plt.plot(plotting_position_time,plotting_position)
# plt.plot(data_sorted['Time to failure'],plotting_position)

N = len(x)  # N is number of points
# print(N)

x_square = []
xy = []
for i in range(N):
    x_square.append(x[i] ** 2)
    xy.append(x[i] * y[i])

sum_x = sum(x)
sum_y = sum(y)
sum_x_square = sum(x_square)
sum_xy = sum(xy)

a = (N * sum_xy - sum_x * sum_y) / (N * sum_x_square - sum_x ** 2)
b = (sum_y - a * sum_x) / N

fx = a * np.asarray(x) + b

# z = np.polyfit(x, y, 1)
# p = np.poly1d(z)

plt.plot(x, y, marker=".")
plt.plot(x, fx, "r--")

plt.title("Weibull plot")
plt.xlabel("log(time)")
plt.ylabel("log(-log(S))")
plt.legend(["Weibull", "y = %.4f*x+%.4f" % (a, b)])

plt.show()
