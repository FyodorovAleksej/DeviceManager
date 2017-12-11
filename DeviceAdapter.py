import re
import subprocess
import os

class DeviceAdapter:
    def getDeviceList(self):
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
                        deviceInfo = {"Name": "", "GUID": "", "HardwareID": "", "Manufacture": "",
                                      "Provider": "",
                                      "Description": "", "sys file": "", "Device Path": ""}
                        deviceInfo["GUID"] = prev
                        for i in re.findall(r"Name:.+\n", descr):
                            deviceInfo["Name"] = deviceInfo["Name"] + i
                        deviceInfo["HardwareID"] = ""
                        for i in re.findall(r"Manufacturer name is.+\n", descr) :
                            deviceInfo["Manufacture"] = deviceInfo["Manufacture"] + i
                        for i in re.findall(r"Provider name is.+\n", descr):
                            deviceInfo["Provider"] = deviceInfo["Provider"] + i
                        for i in re.findall(r"Driver description is.+\n", descr):
                            deviceInfo["Description"] = deviceInfo["Description"] + i
                        for i in re.findall(r"Inf file is.+\n", descr):
                            deviceInfo["Device Path"] = deviceInfo["Device Path"] + i
                        subprocess.call("devcon driverfiles \"@" + prev[:-1] + "\" > " + os.getcwd() + "/sys.txt",
                                        shell=True)
                        sysfile = open(os.getcwd() + "/sys.txt", "r+")
                        systext = sysfile.read()
                        sysfile.close()
                        for i in re.findall(r"\n.+\.sys\n", systext):
                            deviceInfo["sys file"] = deviceInfo["sys file"] + i
                        deviceList.append(deviceInfo)
                    if (line[0] >= '9'):
                        prev = line
                        descr = ""
            else:
                descr = descr + line
        return deviceList

    def enable(self, name):
        subprocess.call("nmcli connection up " + name, shell=True)
        return "Connected to " + name

    def disable(self, name):
        subprocess.call("ping -i 0.2 -c 1 bsuir.by > "+ os.getcwd() + "/ping.txt", shell=True)
        logfile = open(os.getcwd() + "/ping.txt", "r+")
        text = logfile.read()
        text = text.split("--- bsuir.by ping statistics ---")[1]
        logfile.close()
        return text