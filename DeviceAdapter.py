import re
import subprocess
import os

class DeviceAdapter:
    # getting all devices
    def getDeviceList(self):
        # getting information about all devices
        subprocess.call("devcon drivernodes * > " + os.getcwd() + "/devices.txt", shell=True)
        deviceList = []
        devicefile = open(os.getcwd() + "/devices.txt", "r+")
        text = devicefile.readlines()
        devicefile.close()
        prev = ""
        descr = ""
        for line in text:
            if (line[0] != ' '):
                if (line[0] != 'D'):
                    if (prev != ""):
                        # getting info of current device
                        deviceInfo = {"Name": "", "GUID": "", "HardwareID": "", "Manufacture": "",
                                      "Provider": "",
                                      "Description": "", "sys file": "", "Device Path": ""}
                        for i in re.findall(r"Name:.+\n", descr):
                            deviceInfo["Name"] = deviceInfo["Name"] + i.split("Name:")[1]
                        for i in re.findall(r"Inf section is.+\n", descr):
                            deviceInfo["GUID"] = deviceInfo["GUID"] + i.split("Inf section is")[1]
                        deviceInfo["HardwareID"] = prev
                        for i in re.findall(r"Manufacturer name is.+\n", descr) :
                            deviceInfo["Manufacture"] = deviceInfo["Manufacture"] + i.split("Manufacturer name is")[1]
                        for i in re.findall(r"Provider name is.+\n", descr):
                            deviceInfo["Provider"] = deviceInfo["Provider"] + i.split("Provider name is")[1]
                        for i in re.findall(r"Driver description is.+\n", descr):
                            deviceInfo["Description"] = deviceInfo["Description"] + i.split("Driver description is")[1]
                        for i in re.findall(r"Inf file is.+\n", descr):
                            deviceInfo["Device Path"] = deviceInfo["Device Path"] + i.split("Inf file is")[1]
                        subprocess.call("devcon driverfiles \"@" + prev[:-1] + "\" > " + os.getcwd() + "/sys.txt",
                                        shell=True)
                        sysfile = open(os.getcwd() + "/sys.txt", "r+")
                        systext = sysfile.read()
                        sysfile.close()
                        for i in re.findall(r"\n.+\.sys\n", systext):
                            deviceInfo["sys file"] = deviceInfo["sys file"] + i
                        deviceList.append(deviceInfo)
                    # if not a number
                    if (line[0] >= '9'):
                        prev = line
                        descr = ""
            else:
                descr = descr + line
        return deviceList

    # getting status of device
    def refreshStatus(self, hwid):
        subprocess.call("devcon status \"@" + hwid[:-1] + "\" > " + os.getcwd() + "/status.txt", shell=True)
        statusFile = open(os.getcwd() + "/status.txt", "r+")
        text = statusFile.read()
        statusFile.close()
        if ("Driver is running." in text):
            return True
        else:
            return False

    # enabling device by id
    def enable(self, name):
        subprocess.call("devcon /r enable \"@" + name + "\"", shell=True)
        return "enable " + name

    # disabling device by id
    def disable(self, name):
        subprocess.call("devcon /r disable \"@" + name + "\"", shell=True)
        return "disable " + name
