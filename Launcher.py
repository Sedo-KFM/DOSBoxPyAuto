import subprocess
import os

DOSBOX_PATH = 'C:\\Program Files (x86)\\DOSBox-0.74-3\\DOSBox.exe'
CONFIGS_FILE_PATH = 'C:\\Users\\fedor\\AppData\\Local\\DOSBox\\dosbox-0.74-3.conf'
ASM_PATH = 'C:\\Asm\\'
SOURCE_FILE = 'code'

try:
    configs_file_init = open(CONFIGS_FILE_PATH + '_copy.conf', mode='r')
except Exception as e:
    configs_file_init = open(CONFIGS_FILE_PATH + '_copy.conf', mode='w')
    with open(CONFIGS_FILE_PATH, mode='r') as configs_file:
        configs_file_init.writelines(configs_file.readlines())
    configs_file_init.close()
    configs_file_init = open(CONFIGS_FILE_PATH + '_copy.conf', mode='r')
configs_init = configs_file_init.readlines()
configs_file_init.close()
intro = ['mount D C:\\Asm\\',
         'D:']
commands = {'c':['tasm ' + SOURCE_FILE + '.asm',
                 'tlink /t ' + SOURCE_FILE + '.obj'],
            'x': ['tasm ' + SOURCE_FILE + '.asm',
                  'tlink ' + SOURCE_FILE + '.obj'],
            'rc': [SOURCE_FILE + '.com'],
            'rx': [SOURCE_FILE + '.exe'],
            'dc': ['td ' + SOURCE_FILE + '.com'],
            'dx': ['td ' + SOURCE_FILE + '.exe']}
depended_commands = ['r', 'd']
outro = []
boot_conf = str(input(
    'Welcome, are you too lazy?\n' +
    'You have chosen the right way!\n' +
    'c - build to .com\n' +
    'x - build to .exe\n' +
    'r - run\n' +
    'd - debug\n' +
    'q - exit\n' +
    'type your run configuration:\n'))
os.chdir(ASM_PATH)
compiler_mode = ''
while boot_conf != 'q':
    configs = configs_init.copy()
    for intro_com in intro:
        configs.append(intro_com + '\n')
    for boot_coms_abbr in boot_conf:
        if boot_coms_abbr in ['c', 'x']:
            compiler_mode = boot_coms_abbr
        elif boot_coms_abbr in depended_commands:
            if compiler_mode in ['c', 'x']:
                boot_coms_abbr += compiler_mode
            else:
                print('Please, rebuild your project firstly\n')
                break
        try:
            for boot_com in commands[boot_coms_abbr]:
                configs.append(boot_com + '\n')
        except Exception as e:
            print('Unexcepted abbr\n')
            break
    for outro_com in outro:
        configs.append(outro_com + '\n')
    with open(CONFIGS_FILE_PATH, mode='w') as config_file:
        config_file.writelines(configs)
    subprocess.run(DOSBOX_PATH)
    boot_conf = input()
with open(CONFIGS_FILE_PATH, mode='w') as config_file:
    config_file.writelines(configs_init)
os.remove(CONFIGS_FILE_PATH + '_copy.conf')
