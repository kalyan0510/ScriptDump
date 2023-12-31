Task: Make sshfs mount persistant (interms of computer state -  network disconnects, hibernation and sleep etc)  

Task scheduler  

![image](https://github.com/kalyan0510/ScriptDump/assets/14043633/ec92fd59-be21-4113-b48e-5bdc018321d1)  




trigger:  

![image](https://github.com/kalyan0510/ScriptDump/assets/14043633/4c7e968b-7cf9-4659-81b0-a411e10e7be1)


action:  

![image](https://github.com/kalyan0510/ScriptDump/assets/14043633/a6d8db05-3fba-4f35-b771-df92f658a7bd)


%comspec%  
/c start "Title" /min  powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File "C:\Users\gkaly\RunIfNotRunInLastMinute.ps1"
