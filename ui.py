import bimpy 
import fetchHW as f
import tmps as t

ctx = bimpy.Context()
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
            bimpy.set_next_window_pos(bimpy.Vec2(58, 15), bimpy.Condition.Once)
            bimpy.set_next_window_size(bimpy.Vec2(720, 80), bimpy.Condition.Once)
            bimpy.begin("Hardware-Rating")
                        
            bimpy.text("Welcome to Hardware-Rating,")
            bimpy.same_line()
            bimpy.text(f.realUser)
            bimpy.text("Below are your listed computer components and any other useful information per device.")
        
        
            bimpy.set_next_window_pos(bimpy.Vec2(58, 105), bimpy.Condition.Once)
            bimpy.set_next_window_size(bimpy.Vec2(400, 315), bimpy.Condition.Once)
            bimpy.begin("CPU")
            
            bimpy.text("Your CPU is a(n):")
            #try:
            bimpy.text(f.cpu.name)
            bimpy.text("")
            
            
            #for i in range(f.cpu.numberofcores):
                #bimpy.text("Core #{0} - ".format(i+1))
                #bimpy.same_line()
                
            cpuTemps = []
            cpuLoads = []
            
            for j,n in t.oCPULoads.items():
                cpuLoads.append(str(int(n)) + "%")
                # bimpy.text(str(int(n)) + "%")
                # bimpy.text("--------------------------------")
            
            # i=0

            for k,v in t.oCPUTemps.items():      
                bimpy.text(k)
                bimpy.same_line()
                bimpy.text(" -  " + str(v) + " °C  |  ")
                bimpy.text("----------------------------------")
            t.updateCPUInfo()
            
            
            for i in range(len(cpuLoads)):
                bimpy.same_line()   
                bimpy.text(str(cpuLoads[i]))
                # bimpy.text("----------------------------------")
                
                
            # for i in cpuLoads: 
            #     bimpy.same_line()                
            #     bimpy.text(i)
                
            bimpy.set_next_window_pos(bimpy.Vec2(480, 105), bimpy.Condition.Once)
            bimpy.set_next_window_size(bimpy.Vec2(300, 315), bimpy.Condition.Once)
            bimpy.begin("GPU")
            
            bimpy.text("Your GPU is a(n):")
            bimpy.text(f.gpu.name)
                
            