class Corrector:
    def __init__(self):
        pass

    def corrector(self, val): # correct a single value
        if val.isdecimal() and val.isnumeric():
            num = int(val)
            return num
        elif val.capitalize() == 'True':
            return True
        elif val.capitalize() == 'False':
            return False
        elif val.capitalize() == 'None':
            return None
        else:
            return val

    def corrector_list(self, list): # correct a list of values
        temp = []
        for i in list:
            if i.isdecimal() and i.isnumeric():
                num = int(i)
                temp.append(num)
            elif i.capitalize() == 'True':
                temp.append(True)
            elif i.capitalize() == 'False':
                temp.append(False)
            elif i.capitalize() == 'None':
                temp.append(None)
            else:
                temp.append(i)
        return temp