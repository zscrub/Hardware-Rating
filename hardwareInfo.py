import wmi
import time
import bimpy as b
import psutil
import collections
import platform as p
import win32.win32api as w


pcInfo = p.uname()
pcInfo2 = wmi.WMI()

os = pcInfo2.Win32_operatingsystem()[0]
osName = str(os.Name)
osIndex = osName.find("|")
pcName = pcInfo[1]
ver = pcInfo[3]

cpu = pcInfo2.Win32_processor()[0]
gpu = pcInfo2.Win32_videocontroller()[0]
ram = int(os.totalvisiblememorysize)/1000000

user = pcInfo2.win32_computersystem()[0]
userName = str(user.username)
userIndex = userName.find("\\")
realUser = userName[userIndex+1:]


## temps.py
w = wmi.WMI(namespace="root\OpenHardwareMonitor")
pcInfo = w.Hardware()

# Method to check storage remainging however only for main drive??
# hdd = psutil.disk_usage('/')

# print ("Total: {0} GiB".format(hdd.total / (2**30)))
# print ("Used: {0} GiB".format(hdd.used / (2**30)))
# print ("Free: {0} GiB".format(hdd.free / (2**30)))




##################-------FUNCTIONS-------############################# 


def motherBoard():
    mb = ""
    for device in pcInfo:
        if device.HardwareType=="Mainboard":
            mb = device.name
    return mb        
  
def storageDevices():
    storageDevicesList = [] 
    for device in pcInfo:
        if device.HardwareType=="HDD":
            storageDevicesList.append(device.name)
    return storageDevicesList

def storageLoad():
    storageLoadList = []
    for sensor in w.Sensor():
        for device in  pcInfo:    
            if sensor.sensortype =="Load" and device.HardwareType=="HDD":
                storageLoadList.append([sensor.name, sensor.value])
    return storageLoadList


## CHANGE IF STATEMENT TO BETTER FETCH THE INFORMATION (instead of sensor.name[0], check sensor.hardwareType?)
def cpuTemps():
    tcpuTempsList = []
    for sensor in w.Sensor():
        if sensor.sensortype =="Temperature" and sensor.name[0]=="C":      
            tcpuTempsList.append([sensor.name, sensor.value])
    return tcpuTempsList


def cpuLoads():
    tcpuLoadsList = []
    for sensor in w.Sensor():
        if sensor.sensortype =="Load" and sensor.name[0]=="C":
            tcpuLoadsList.append([sensor.name, sensor.value])
    return tcpuLoadsList


def cpuClocks():
    tcpuClocksList = []
    for sensor in w.Sensor():
        if sensor.sensortype =="Clock" and sensor.name[0]=="C":
            tcpuClocksList.append([sensor.name, sensor.value])
    return tcpuClocksList


def gpuTemps():                
    tgpuTempsList = []
    for sensor in w.Sensor():
        if sensor.sensortype =="Temperature" and sensor.name[0]=="G":
            tgpuTempsList.append([sensor.name, sensor.value])
    return tgpuTempsList


def gpuClocks():
    tgpuClocksList = []
    for sensor in w.Sensor():
        if sensor.sensortype =="Clock" and sensor.name[0]=="G":
            tgpuClocksList.append([sensor.name, sensor.value])
    return tgpuClocksList
#####################################################################################

##  ui.py
ctx = b.Context()
ctx.init(800, 450, "Hardware Rating")

### Create a function to that fetches every temp and put it in a dict or anything else.
### Then run that function on a second thread
## AKA
# import threading

# def fetchTempFunction():
#   return to array and use the array to fill in the values
# cool_thread = threading.Thread(target = fetchTempFunction())
# cool_thread.start()

if __name__ == "__main__":
    while(not ctx.should_close()):
        with  ctx:
            w.Sensor()
            
            # intro window
            b.set_next_window_pos(b.Vec2(12, 15), b.Condition.Once)
            b.set_next_window_size(b.Vec2(765, 80), b.Condition.Once)
            b.begin("Hardware-Rating")
                        
            b.text("Welcome to Hardware-Rating,")
            b.same_line()
            b.text(realUser)
            b.text("Below are your listed computer components and any other useful information per device.")
        
            # CPU window
            b.set_next_window_pos(b.Vec2(12, 100), b.Condition.Once)
            b.set_next_window_size(b.Vec2(435, 325), b.Condition.Once)
            b.begin("CPU")
            
            b.text("Your CPU is a(n):")
            #try:
            b.text(cpu.name)
            b.text("")

            gpuClocksList = gpuClocks()
              
            for i in range(len(cpuTemps())):
                cpuTempsList = cpuTemps()
                gpuTempsList = gpuTemps()
                cpuLoadsList = cpuLoads()
                cpuClocksList = cpuClocks()
                b.text(cpuTempsList[i][0])
                b.same_line()
                b.text(" - " + str(int(cpuTempsList[i][1])) + "°C  |  Load: " + str(int(cpuLoadsList[i][1])) + "%  |  " + str(int(cpuClocksList[i-1][1])) + " MHz")
                b.text("--------------------------------------------------------------")

            # GPU Window    
            b.set_next_window_pos(b.Vec2(450, 100), b.Condition.Once)
            b.set_next_window_size(b.Vec2(330, 230), b.Condition.Once)
            b.begin("GPU")
            
            b.text("Your GPU is a(n):")
            b.text(gpu.name)
            b.text("")
            
            gpuTempsList = gpuTemps()
            
            for i in range(len(gpuTempsList)):
                b.text(str(gpuTempsList[i][0]) + "  |  " + str(gpuTempsList[i][1]) + "°C  ")
                b.text("-------------------------------------------")
            
            
            for i in range(len(gpuClocksList)):
                b.text(str(gpuClocksList[i][0]) + " Speed  |  " + str(int(gpuClocksList[i][1])) + " MHz")
                b.text("-------------------------------------------")
                
              
            # Ram Window
            b.set_next_window_pos(b.Vec2(450, 325), b.Condition.Once)
            b.set_next_window_size(b.Vec2(330, 100), b.Condition.Once)
            b.begin("Storage")
            b.text("Memory: " + str(int(ram)) + "GB")
            # b.text(storageLoad())
            
            for i in range(len(storageDevices())):
                storageUnitList = storageDevices()
                b.text(storageUnitList[i])