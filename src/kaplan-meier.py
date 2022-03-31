import pandas as pd
import matplotlib.pyplot as plt

filename = "Data_for_analysis.xlsx"

data = pd.read_excel(filename, skiprows=2)
data_sorted = data[["Time to failure", "Action"]].sort_values(
    by="Time to failure", ignore_index=True
)

# print(data_sorted) #printing an array with the Time column
# print(len(data_sorted))

rows = len(data_sorted)  # 196
# print(rows)

n = []
for i in range(rows, 0, -1):
    if data_sorted["Action"][rows - i] == "S":
        n.append(None)
        continue
    else:
        n.append(i)
    # print(i)

# print(n)  # printing an array with the n elements
# print(len(n))

D = []
for i in range(rows):
    if data_sorted["Action"][i] == "S":
        D.append(None)
        continue
    else:
        D.append(1)
    # print(i)

# print(D)
# print(len(D))

S = []
last_element = 1
for i in range(rows):
    if data_sorted["Action"][i] == "S":
        S.append(None)
        continue
    else:
        value = last_element * (1 - D[i] / n[i])
        last_element = value
        S.append(value)

# print(S) #printing an array with the S column
# print(len(S))

t = []
for i in range(rows):
    if D[i] == None:
        t.append(None)
        continue
    else:
        t.append(data_sorted["Time to failure"][i])

# print(t) # failure time
# print(len(t))

x = []
y = []
for i in range(rows):
    if t[i] != None and S[i] != None:
        x.append(t[i])
        y.append(S[i])

plt.step(x, y)

plt.title("Kaplan-Meier")
plt.xlabel("Elapsed time(days)")
plt.ylabel("Probability of surviving")

plt.show()
