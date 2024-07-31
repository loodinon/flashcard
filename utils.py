def read_setting():
    with open('setting.txt', 'r') as file:
        lines = file.readlines()
        mw = int(lines[0].split(":")[1].strip())
        mode = lines[1].split(":")[1].strip()
    return (mw, mode)