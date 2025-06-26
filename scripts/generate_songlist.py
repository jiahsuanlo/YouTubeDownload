
# fname = "input/yellowstone_list.txt"
fname = "input/jia_list.txt"

with open(fname, "r") as fid:
    lines = fid.readlines()


for line in lines:
    if line.strip() == "":
        continue
    items = [x.strip() for x in line.split(",")]
    print(f'- ["{items[1]}", "{items[0]}"]')