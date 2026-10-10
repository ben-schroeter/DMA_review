import re, sys
M = {"D97757": "B8860B", "141413": "282424", "E6E3D9": "E8E6E3", "6B6A64": "666666", "3D3D3A": "3F3B3B",
     "F4F2EC": "F5F5F0", "D5D2C6": "D4D2CE", "B85C3F": "8F6708", "5E5D59": "5C5858", "D4A85A": "D9BE7A", "5E7FA8": "004494",
     "A9A79D": "A6A3A0", "7D9B76": "7FA3CC", "BDBAAE": "C4C1BE", "EDE6D8": "EFEBDD", "6A6A64": "666262", "C9C6BA": "C9C6C3",
     "8F4A33": "8F6708", "7A786F": "777373", "EEECE4": "F0EFEA", "EDB9A3": "E3CF9C", "9C9A92": "9A9696"}
for p in sys.argv[1:]:
    s = open(p).read()
    s2 = re.sub(r"#([0-9A-Fa-f]{6})\b", lambda m: "#" + M.get(m.group(1).upper(), m.group(1)), s)
    open(p, "w").write(s2); print(p, s != s2)
