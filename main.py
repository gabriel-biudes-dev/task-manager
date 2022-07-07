import psutil, os

memory = psutil.virtual_memory()
disk = psutil.disk_usage('/')
temperatures = psutil.sensors_temperatures()
users = psutil.users()

#Concerte o valor de byte para gigabyte
def convert(value):
    return value / 1024 / 1024 / 1024

#Mostra informações da memória 
def showMemory():
    total_memory = convert(memory.total)
    available_memory = convert(memory.available)
    used_memory = convert(memory.used)
    percent_memory = memory.percent
    print("[MEMORY STATUS]")
    print("Total memory: %.2f" %total_memory + " GB")
    print("Available memory: %.2f" %available_memory + " GB")
    print("Used memory: %.2f" %used_memory + " GB")
    print("Percentage of memory used: " + str(percent_memory) + "%")

#Mostra informações do disco principal 
def showDisk():
    total_space = convert(disk.total)
    used_space = convert(disk.used)
    free_space = convert(disk.free)
    percent_space = disk.percent

    print("[STORAGE STATUS]")
    print("Total space: %.2f" %total_space + " GB")
    print("Used space: %.2f" %used_space + " GB")
    print("Free space: %.2f" %free_space + " GB")
    print("Percentage of storage used: " + str(percent_space) + "%")

#Mostra a temperatura da CPU
def showTemperatures():
    print("[CPU TEMPERATURES]")
    for x in temperatures['coretemp']:
        print(x.label)
        print(x.current)
        print('')

#Mostra os usuários do sistema
def showUsers():
    for user in users:
        print("Name: " + user.name)
        print("Host: " + user.host)
        print("Pid: " + str(user.pid))
        print("")

#Retorna o tamanho da maior string em uma propriedade de uma lista
def getBigger(list, prop):
    max = 0
    for x in list:
        value = str(x.info[prop])
        if(len(value) > max): max = len(value)
    return max

#Mostra os processos rodando na máquina 
def showProcesses():
    maxPidSize = getBigger(psutil.process_iter(['pid', 'name', 'username']), 'pid')
    maxNameSize = getBigger(psutil.process_iter(['pid', 'name', 'username']), 'name')
    maxUserSize = getBigger(psutil.process_iter(['pid', 'name', 'username']), 'username')
    print('[PID]', end = '')
    for x in range(maxPidSize - 2): print(' ', end = '')
    print('[NAME]', end = '')
    for x in range(maxNameSize): print(' ', end = '')
    print('[USER]', end = '')
    for x in range(maxUserSize - 3): print(' ', end = '')
    print('[MEMORY USAGE]')
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        print(str(proc.info['pid']), end = '')
        for x in range(maxPidSize - len(str(proc.info['pid'])) + 3): print(' ', end = '')
        print(proc.info['name'] + '   ', end = '')
        for x in range(maxNameSize - len(proc.info['name']) + 3): print(' ', end = '')
        print(proc.info['username'], end = '')
        for x in range(maxUserSize - len(proc.info['username']) + 3): print(' ', end = '')
        print("%.2f" %proc.memory_percent() + "%")

#Retorna uma lista com todos os processos com certo nome ou com certo PID
def findProcess(method, process):
    list = []
    if method == 'pid': process = int(process)
    for p in psutil.process_iter([method]):
        if p.info[method] == process: list.append(p)
    return list

#Finaliza um processo
def killProcess(method):
    p = input('Enter the process ' + method + ': ')
    list = findProcess(method, p)
    if not list: print('No such process was found running on the system')
    for x in list:
        x.kill()
        print('Process ' + p + ' killed')

#Mostra o menu
def showMenu():
    print("\n1)Show memory status")
    print("2)Show storage status")
    print("3)Show CPU temperatures")
    print("4)Show users info")
    print("5)Show processes information")
    print("6)Kill process by name")
    print("7)Kill process by PID")
    print("8)Exit")
    answer = int(input("Operation code: "))
    os.system('clear')
    return answer

def main():
    opt = 1
    while opt != 8:
        opt = showMenu()
        print("")
        if opt == 1: showMemory()
        if opt == 2: showDisk()
        if opt == 3: showTemperatures()
        if opt == 4: showUsers()
        if opt == 5: showProcesses()
        if opt == 6: killProcess('name')
        if opt == 7: killProcess('pid')

main()
