import os
from pathlib import Path

def print_tree(startpath, level=0):
    for item in sorted(os.listdir(startpath)):
        path = os.path.join(startpath, item)
        # print(path)


        if item.startswith('.') or item == 'myenv' or item == '__pycache__':
            continue

        if os.path.isdir(path):
            print('│   ' * level + '├── ' + item)
            print_tree(path, level + 1)
        else:
            if level == 0:  # ✅ Only print files in the top-level directory
                print('│   ' * level + '├── ' + item)

# path = Path(__file__).parents[0]
# print(path)
path = Path(__file__).parents[1]
print(path)
print_tree(path)