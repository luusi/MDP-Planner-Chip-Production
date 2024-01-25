import glob

files = glob.glob('*.log')

for file in files:
    file_l = file.split('_')
    
    mode = file_l[-3]
    new_mode = ""
    if mode == 'small':
        new_mode = "xsmall"
    elif mode == 'medium':
        new_mode = "small"
    elif mode == 'large':
        new_mode = "medium"
    elif mode == 'xlarge':
        new_mode = "large"

    file_l[-3] = new_mode

    new_file = "_".join(file_l[5:])

    with open(file, 'r') as f:
        lines = f.readlines()
    with open(new_file, 'w') as f:
        f.writelines(lines)