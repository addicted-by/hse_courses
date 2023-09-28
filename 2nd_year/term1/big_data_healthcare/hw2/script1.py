import os
from collections import defaultdict



FOLDER = './Clinical_HL7_Samples'
assert os.path.exists(FOLDER), f"{FOLDER} does not exist."


def get_bday(path: str) -> str:
    f = open(path, 'r')
    text = f.read()
    f.close()
    segments = text.split('\n')
    for seg in segments:
        if seg.startswith("PID"):
            bday = seg.split('|')[7]
    return bday

if __name__ == "__main__":
    birthday = defaultdict(str)
    for root, d_names, f_names in os.walk(FOLDER):
        for file in f_names:
            path2file = os.path.join(root, file)
            bday = get_bday(path2file)
            if bday:
                birthday[path2file] = bday
            else:
                print(f"Cannot process the file {path2file}")

    birthday = sorted(birthday.items(), key=lambda x:x[1], reverse=True)
    print("The youngest", birthday[0][1])

# for file, bday in birthday.items():
#     print(file, bday)