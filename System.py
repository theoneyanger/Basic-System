# MODULE TIME
import json as j
import FileManager as Fm
import os
from datetime import datetime
import Val_Corrector as Vc
from termcolor import cprint
try:
    class System:
        def __init__(self):
            self.file_manager = Fm.FileManager()
            self.corrector = Vc.Corrector()
            self.file_manager.change_dir("File_Env")
            with open("Save.json", 'r') as f:
                try:
                    self.system_variables = j.load(f)
                except:
                    self.system_variables = {}
            with open("History.json", 'r') as f:
                try:
                    self.history = j.load(f)
                except:
                    self.history = []
            with open("Functions.json", 'r') as f:
                try:
                    self.functions = j.load(f)
                except:
                    self.functions = {}
            with open("Users.json", 'r') as f:
                try:
                    self.users = j.load(f)
                except:
                    self.users = {}
            with open("Settings.json", 'r') as f:
                try:
                    self.cur_color = j.load(f)
                except:
                    self.cur_color = 'white'
            self.ALLOWED_EXTENSIONS = ['.txt', '.json', '.csv', '.md', '.py']
            self.commands = ['-add_var variable value',
                             '-get_var variable name',
                             '-help',
                             '-exit',
                             '-vars',
                             '-update_var variable new_value',
                             '-del_var variable name',
                             "-history",
                             "-del_history",
                             "-load_file file name",
                             '-make_file file name',
                             '-change_dir new directory',
                             "-func name command1|command2|command3...",
                             '-dir',
                             "-remove_file filename",
                             "-run_func function name",
                             '-funcs_show',
                             '-edit_func name new command',
                             '-del_func',
                             "-remove filename",
                             "-write file content"
                             '-echo message or variable',
                             "-hard_save",
                             "-time",
                             "-clear",
                             "-color_set new",
                             "-colors",
                             "-hard_delete",
                             '-operation number or variable arithmetic symbol number or variable']
            self.color_available = [
                "black",
                "red",
                "green",
                "yellow",
                "blue",
                "magenta",
                "cyan",
                "white",
                "light_grey",
                "dark_grey",
                "light_red",
                "light_green",
                "light_yellow",
                "light_blue",
                "light_magenta",
                "light_cyan"
            ]

        def add_var(self, name, value):
            self.system_variables[name] = value

        def retrieve_var(self, name):
            try:
                return self.system_variables[name]
            except KeyError:
                return f"Variable {name} not found"

        def update_var(self, name, new_value):
            if name in self.system_variables:
                self.system_variables[name] = new_value
            else:
                return f"Variable {name} not found"

        def del_var(self, name):
            if name in self.system_variables:
                del self.system_variables[name]
            else:
                return f"Variable {name} not found"

        def vars(self):
            temp = ''
            for key, value in self.system_variables.items():
                temp += f"{key} = {value}\n"
            return temp

        def time(self):
            time = datetime.now()
            time = time.strftime("%H:%M:%S")
            return time

        def operations(self, command):
            try:
                if command[1] in self.system_variables.keys():
                    num1 = int(self.system_variables[command[1]])
                else:
                    num1 = int(command[1])
                if command[3] in self.system_variables.keys():
                    num2 = int(self.system_variables[command[3]])
                else:
                    num2 = int(command[3])
                if command[2] == '+':
                    return f"{num1} + {num2} = {num1 + num2}"
                elif command[2] == '-':
                    return f"{num1} - {num2} = {num1 - num2}"
                elif command[2] == '*':
                    return f"{num1} * {num2} = {num1 * num2}"
                elif command[2] == '/':
                    return f"{num1} / {num2} = {num1 / num2}"
                elif command[2] == '**' or command[2] == '^':
                    return f"{num1} ^ {num2} = {num1 ** num2}"
                elif command[2] == '%':
                    return f"{num1} % {num2} = {num1 % num2}"
            except ValueError:
                try:
                    int(command[1])
                except ValueError:
                    return f"No variable with name {command[1]}"
                except TypeError:
                    return f"Variable {command[1]} is a string"
                try:
                    int(command[3])
                except ValueError:
                    return f"No variable with name {command[3]}"
                except TypeError:
                    return f"Variable {command[3]} is a string"

        def show_history(self):
            temp = ''
            for i in self.history:
                temp += i
            return temp

        def del_history(self):
            self.history.clear()

        def create_func(self, name, command):
            temp_command = ''
            for i in command:
                temp_command += f'{i} '
            self.functions[name] = temp_command.strip()

        def run_func(self, name):
            try:
                if "|" in self.functions[name]:
                    temp = self.functions[name].split("|")
                    self.execute_commands(temp)
                else:
                    self.proc_comm(self.functions[name].split(), name)
            except KeyError:
                print(f"No function with name {name}")

        def funcs(self):
            for k, v in self.functions.items():
                print(f"{k}: {v}")

        def edit_func(self, name, new):
            if not self.functions.get(name, False):
                print(f"No function named {name}")
            else:
                self.functions[name] = new

        def del_func(self, name):
            if not self.functions.get(name, False):
                cprint("No function named {name}", self.cur_color)
            else:
                del self.functions[name]

        def echo(self, message):
            if isinstance(message, str):
                if message in self.system_variables:
                    cprint(self.system_variables[message], self.cur_color)
                else:
                    cprint(message, self.cur_color)
            elif isinstance(message, list):
                joined_message = ' '.join(message)
                if joined_message in self.system_variables:
                    cprint(self.system_variables[joined_message], self.cur_color)
                else:
                    cprint(" ".join(message), self.cur_color)

        def clear(self):
            os.system('cls')

        def exit_system(self):
            self.hard_save()
            exit()

        def color_set(self, new):
            if new in self.color_available:
                self.cur_color = new
            else:
                cprint(f"Invalid color {new}", self.cur_color)

        def hard_save(self):
            with open(f"Save.json", 'w') as f:
                j.dump(self.system_variables, f)
            with open(f"History.json", 'w') as f:
                j.dump(self.history, f)
            with open(f"Functions.json", 'w') as f:
                j.dump(self.functions, f)
            with open(f"Users.json", 'w') as f:
                j.dump(self.users, f)
            with open(f"Settings.json", 'w') as f:
                j.dump(self.cur_color, f)

        def hard_delete(self):
            with open(f"Save.json", 'w') as f:
                j.dump('', f)
                self.system_variables = {}
            with open(f"History.json", 'w') as f:
                j.dump('', f)
                self.history = []
            with open(f"Functions.json", 'w') as f:
                j.dump('', f)
                self.functions = {}
            with open(f"Users.json", 'w') as f:
                j.dump('', f)
                self.users = {}
            with open(f"Settings.json", 'w') as f:
                j.dump('', f)
                self.cur_color = 'white'

        def make_file(self, name):
            if self.file_manager.check_file(name, self.ALLOWED_EXTENSIONS[:]):
                self.file_manager.make_file(name)
            else:
                cprint("Invalid file extension", self.cur_color)

        def dir(self):
            return self.file_manager.get_dir()

        def change_dir(self, new):
            self.file_manager.change_dir(new)

        def remove(self, name):
            self.file_manager.remove_file(name)

        def repair_files(self):
            missing_files = []
            system_files = ["History.json", "Users.json", "Save.json", "Functions.json", 'Settings.json']
            for i in system_files:
                if i not in system_files:
                    missing_files.append(i)
            if missing_files:
                cprint("CRITICAL ERROR: Missing system files:\n", self.cur_color)
                for i in missing_files:
                    cprint(i, self.cur_color)
            self.hard_save()

        def create_us(self):  # us stands for user, not the US!
            cprint("Select name for new user:", self.cur_color)
            name = input()
            cprint(f"Select password for {name}:", self.cur_color)
            passw = input()
            choice = ''
            while choice != passw:
                cprint("Confirm password:", self.cur_color)
                choice = input()
            cprint(f"Successfully created user named {name} with password {passw}", self.cur_color)
            self.users[name] = passw
            self.user()

        def login(self):
            cprint("Select user to login as:", self.cur_color)
            name = input()
            if name in self.users.keys():
                cprint(f"Enter password for {name}:", self.cur_color)
                passw = input()
                if passw == self.users[name]:
                    pass
                else:
                    print("Invalid password")
                    self.user()
            else:
                cprint(f"Could not find user {name}", self.cur_color)
                self.user()

        def user(self):
            if not self.users:
                cprint("No users found. Creating new user...", self.cur_color)
                self.create_us()
            else:
                cprint("1. Create new user\n2. Login as existing user\n3. Forgot password of a user\n", self.cur_color)
                choice = input()
                if choice == '1':
                    self.create_us()
                elif choice == '2':
                    for i in self.users.keys():
                        cprint(i, self.cur_color)
                    print("\n")
                    self.login()
                elif choice == '3':
                    cprint("Available users", self.cur_color)
                    for i in self.users.keys():
                        print(i)
                    print("\n")
                    cprint("Select user:", self.cur_color)
                    choice = input()
                    cprint(f"Password of {choice}: {self.users[str(choice)]}", self.cur_color)
                    self.user()
                else:
                    cprint("Invalid input", self.cur_color)
                    self.user()
                self.ask_comm()

        def ask_comm(self):
            cprint("Use -help for help", self.cur_color)
            command = input()
            command_split = command.split()
            self.proc_comm(command_split, command)

        def proc_comm(self, command, original_command, ask_next=True):
            self.repair_files()
            self.hard_save()
            try:
                self.history.append(f"{original_command}\n")
                if command[0] == '-add_var':
                    self.add_var(command[1], command[2])
                elif command[0] == 'N':
                    self.ask_comm()
                elif command[0] == '-get_var':
                    cprint(self.retrieve_var(command[1]), self.cur_color)
                elif command[0] == '-help':
                    for i in self.commands:
                        cprint(f"{i}\n", self.cur_color)
                elif command[0] == '-exit':
                    self.hard_save()
                    exit()
                elif command[0] == '-del_var':
                    self.del_var(command[1])
                elif command[0] == '-update_var':
                    self.update_var(command[1], command[2])
                elif command[0] == '-vars':
                    cprint(self.vars(), self.cur_color)
                elif command[0] == '-operation':
                    cprint(self.operations(command), self.cur_color)
                elif command[0] == '-history':
                    cprint(self.show_history(), self.cur_color)
                elif command[0] == '-del_history':
                    self.del_history()
                elif command[0] == '-make_file':
                    self.make_file(command[1])
                elif command[0] == '-dir':
                    cprint(self.dir(), self.cur_color)
                elif command[0] == '-change_dir':
                    self.change_dir(command[1])
                elif command[0] == '-func':
                    self.create_func(command[1], command[2:])
                elif command[0] == '-run_func':
                    self.run_func(command[1])
                elif command[0] == '-del_func':
                    self.del_func(command[1])
                elif command[0] == '-funcs_show':
                    self.funcs()
                elif command[0] == '-edit_func':
                    self.edit_func(command[1], command[2:])
                elif command[0] == '-echo':
                    self.echo(command[1:])
                elif command[0] == '-clear':
                    self.clear()
                elif command[0] == '-hard_delete':
                    self.hard_delete()
                elif command[0] == '-time':
                    cprint(self.time(), self.cur_color)
                elif command[0] == '-remove_file':
                    self.remove(command[1])
                elif command[0] == '-color_set':
                    self.color_set(command[1])
                elif command[0] == '-colors':
                    for i in self.color_available:
                        cprint(i, i)
                else:
                    cprint(f"Could not understand command {original_command}", self.cur_color)
                if ask_next:
                    self.ask_comm()
            except IndexError:
                cprint(f"Missing arguments for command {original_command}", self.cur_color)
                if ask_next:
                    self.ask_comm()

        def execute_commands(self, commands_list):
            for command in commands_list:
                comm_split = command.split()
                self.proc_comm(comm_split, command, ask_next=False)
            self.ask_comm()


    sys = System()
    sys.user()
except KeyboardInterrupt:
    print(f"Oops")
    sys.hard_save()