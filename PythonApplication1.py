import ahkab as ak
import numpy as np

f = open("input.txt","r")   

circ = ak.Circuit(title="a")

freq = 50

while True :
    line = f.readline() 
    if len(line) == 0:
        break  # check for EOF
    line = line.strip().lower()
                
    if len(line) == 0:
        continue  # empty line is really empty after strip()

    l=line.split()
    
    if not l[1] =="0" :
        n1 = "n"+l[1]
    else :
        n1 = circ.get_ground_node()  
        
    if not l[2]=="0" :
        n2 = "n"+l[2]
    else :
        n2 = circ.get_ground_node()  
        
    n3 = float(l[3])
              
    if line[0] == "v" or line[0] == "V": 
        n4 = float(l[4])
        circ.add_vsource(l[0],n1,n2,dc_value=0,ac_value=n3*(np.cos(np.pi*n4/180.0)+1j*np.sin(np.pi*n4/180.0)))
        continue
    
    elif line[0] == "i" or line[0] == "I": 
        n4 = float(l[4])
        circ.add_isource(l[0],n1,n2,dc_value=0,ac_value=n3*(np.cos(np.pi*n4/180.0)+1j*np.sin(np.pi*n4/180.0)))
        continue
    
    elif line[0] == "c" or line[0] == "C": 
        circ.add_capacitor(l[0],n1,n2,float(l[3]))
        continue
    
    elif line[0] == "l" or line[0] == "L": 
        circ.add_inductor(l[0],n1,n2,float(l[3]))
        continue
    
    elif line[0] == "r" or line[0] == "R": 
        circ.add_resistor(l[0],n1,n2,float(l[3]))
        continue
    

#print(circ)

f.close()
             
ac = ak.new_ac(start=freq,stop=freq,points=2,x0=None)

res = ak.run(circ,ac)


#for x in res['ac'] :
#    print(x[0],':',abs(x[1][0]))
     

f = open("input.txt","r")
out=open ("output.txt","w")
while True :
    line = f.readline() 
    if len(line) == 0:
        break  # check for EOF
    line = line.strip().lower()
                
    if len(line) == 0:
        continue  # empty line is really empty after strip()

    l=line.split()
    
    if not l[1] =="0" :
        n1 = "n"+l[1]
        string = "V"+n1    
        v1 = res['ac'][string][0]

    else :
        n1 = circ.get_ground_node()  
        v1 = 0

    if not l[2]=="0" :
        n2 = "n"+l[2]
        string2 = "V"+n2
        v2 = res['ac'][string2][0]

    else :
        n2 = circ.get_ground_node()  
        v2 = 0

    n3 = float(l[3])  
    
    v = v1-v2

    if line[0] == "v" or line[0] == "V": 
        st = 'I('+l[0]+')'
        i = res['ac'][st][0]
        z = n3 / i

    elif line[0] == "i" or line[0] == "I": 
        z = v / n3
        
    elif line[0] == "c" or line[0] == "C": 
        z = 1.000/(1j*2*np.pi*freq*n3)  
            
    elif line[0] == "l" or line[0] == "L": 
        z = 1j*np.pi*2*freq*n3    
        

    elif line[0] == "r" or line[0] == "R": 
        z = n3
        

        
    p = abs(np.power(v,2)/(2.0*z))
    
    p = "{0:.12f}".format(p)
    
 #   x =''
 #   if v2 > v1 and (line[0] == "v" or line[0] == "V" or line[0] == "i" or line[0] == "I") :
 #       x = '-'
    s = "Power ("+l[0] +") = " + str(p)
        
    if line[0] == "l" or line[0] == "L": 
            s = "Power ("+l[0] +") = " + '- '  + str(p) + "  VAR"

    elif line[0] == "c" or line[0] == "C": 
        s = s + "  VAR"

    elif line[0] == "r" or line[0] == "R": 
        s = s + "  Watt"

    elif line[0] == "v" or line[0] == "V" or line[0] == "i" or line[0] == "I": 
        x =''
        if abs(v2) > abs(v1) and (line[0] == "v" or line[0] == "V" or line[0] == "i" or line[0] == "I") :
            x = '-'
        s = "Power ("+l[0] +") = " + x + str(p) + "  VA"


    print(s)
    out.write(s)
    out.write('\n')




f.close()
out.close()