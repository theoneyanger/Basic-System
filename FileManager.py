import os
class FileManager:
    def __init__(self):
        pass

    def make_file(self, name, allowed):
        if os.path.splitext(name)[1] in allowed:
            f = open(name, 'x')
            f.close()
            return True
        else:
            return False

    def remove(self, name):
        os.remove(name)

    def get_dir(self):
        return os.getcwd()

    def change_dir(self, dir):
        try:
            os.chdir(dir)
            return True
        except Exception as e:
            return e


if __name__ == '__main__':
    filemanager = FileManager()
    ALLOWED_EXTENSIONS = ['.txt', '.json', '.csv', '.md', '.py']
    print(filemanager.make_file('Hi.txt', ALLOWED_EXTENSIONS))