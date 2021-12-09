with open("input.txt", "r") as f:
    data = f.readlines()
data = [e.strip() for e in data]
cnt = 0
for i in range(1, len(data)):
    if int(data[i]) > int(data[i - 1]):
        cnt += 1
print(cnt)
