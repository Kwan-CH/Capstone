import os

def print_tree(startpath, level=0):
    for item in sorted(os.listdir(startpath)):
        path = os.path.join(startpath, item)

        if item.startswith('.') or item == 'myenv':
            continue

        if os.path.isdir(path):
            print('│   ' * level + '├── ' + item)
            print_tree(path, level + 1)

print_tree('C:\\Users\Hp\Desktop\Capstone Assignment\Capstone')
