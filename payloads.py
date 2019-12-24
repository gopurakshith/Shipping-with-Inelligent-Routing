import math 

#path = input("Enter the desired path: ")
path = ['a','b','f','d','e','g']
length=len(path)
path_city_prty =  [[0 for x in range(2)] for y in range(length)]   #declaring 2d list with size
for i in range(length):
    path_city_prty[i][0] = i
    path_city_prty[i][1] = path[i]
max_truck_load = 1000
coordinates= [(5,6,'a'), (1,2,'b'), (3,4,'c'), (2,3,'d'), (3,5,'e'),(2,5,'f'),(1,3,'g')]

#code for sorting coordinates according to the final path
no_of_routes = 0

while no_of_routes == 0:
    try:
        no_of_routes = int(input("Enter the number of routes: "))
    except ValueError:
        print("Oops! That was not a Valid Number, please enter again")

route=[[0 for x in range(2)] for y in range(no_of_routes)] 
#print(route)
weight=[[0 for x in range(2)] for y in range(no_of_routes)] 
route_stops=[]
#cost = []
kg_per_km = 1
for i in range(no_of_routes):
    if i == 0:
        route[i] = input("Enter the primary route: ")
        weight[i] = input("Enter the Weight: ")
    else:    
        route[i] = input("Enter the route: ")
        weight[i] = input("Enter the Weight: ")
j=0
x1 = 0
y1 = 0
x2 = 0
y2 = 0
temp = 1.00   #for keeping the primary route at the top

j = len(route[j])
y = 0
route_lenth = len(route)
cost = [[0 for x in range(4)] for y in range(no_of_routes)] 
for i in range(route_lenth):
    #print("main: ",i)
    for y in range(length):
        #print("Submain1: ",y)
        #print(route[i][0])
        #print(coordinates[y][2])
        if route[i][0]==coordinates[y][2]:   # route = ab , coord = a
            x1 = coordinates[y][0]
            y1 = coordinates[y][1]
            #print("Hello1")
            #print(x1,"+",y1)
    for y in range(length):
        #print("Submain2: ",y)
        if route[i][1]==coordinates[y][2]:
            #print("Hello2")
            x2 = coordinates[y][0]
            y2 = coordinates[y][1]
            #print(x2,"+",y2)
    
    if i==0 :
        cost[i][0] =  float(math.sqrt( (x2-x1)**2 + (y2-y1)**2 )) * float(weight[i]) * kg_per_km*10000
        temp = float(math.sqrt( (x2-x1)**2 + (y2-y1)**2 )) * float(weight[i]) * kg_per_km
    else:
        cost[i][0] =  float(math.sqrt( (x2-x1)**2 + (y2-y1)**2 )) * float(weight[i]) * kg_per_km
    cost[i][1] = float(weight[i])
    cost[i][2] =  route[i][0]          #route allocation, ex: ab --> a
    cost[i][3] =  route[i][1]          #route allocation, ex: ab --> b

#print(cost)    

cost.sort(reverse = True) 
cost[0][0] = temp                                     #special modification for primary route
#print("Cost:  Weight:   Start point:  End Point:")
#print(cost)

load_path = [[0 for x in range(4)] for y in range(no_of_routes)] 
selected_path = [[0 for x in range(4)] for y in range(no_of_routes)] 
selected_path_s = []
selected_path_e = []
selected_weight = []
#selected_weight[1]= cost[0][1]
                              #swap for primary path
load_path[0] = cost[0]
#print(load_path[0])

load_path_load = 0            #for finding the total load in entire path
cal_load = 0                  #for calculating if the added load in if,elif is below the limit
limit  = 1000
may_over_load = 0

load_path_load = cost[0][1]       #as first load gets loaded automatically
selected_path_s.append(cost[0][2])
selected_path_e.append(cost[0][3])
selected_weight.append(cost[0][1])

#print("Initial Load: ", load_path_load)
count = 1
for j in range(no_of_routes):
    #print("main: ", j)
    for i in range(j):
        #if(i==0):
            #i=1
        #print("sub: ", i)
        fcs = cost[i][2]     #First Character start point
        fce = cost[i][3]     #First Character start point
        #print("F: ", fcs,fce)

        scs = cost[j][2]    #Second Character start point
        sce = cost[j][3]    #Second Character start point
        sl = cost[j][1]     #load added in this route
        #print("S: ", scs, sce, sl)
        

        if ((path.index(scs)>path.index(fcs)) and (path.index(scs)<path.index(fce))):
            #print("first point inside")
            may_over_load = 1

        elif ((path.index(sce)>path.index(fcs)) and (path.index(sce)<path.index(fce))):
            #print("Second point inside")
            may_over_load = 1

        else:                 # check for i+1 in index if necessary
            #print("going ok")
            load_path_load = load_path_load + cost[j][1]
            if load_path_load > limit:
                load_path_load = load_path_load - cost[j][1]
                             #route weight
            else:
                selected_path_s.append(scs)              #route strating point
                selected_path_e.append(sce)              #route ending point
                selected_weight.append(sl) 
                #print(sl)

        if may_over_load == 1:
            may_over_load = 0
            load_path_load = load_path_load + cost[j][1]
            if load_path_load > limit:
                load_path_load = load_path_load - cost[j][1]
                             #route weight
            else:
                selected_path_s.append(scs)              #route strating point
                selected_path_e.append(sce)              #route ending point
                selected_weight.append(sl) 
                print(sl)

           #testing2 code here
            
    

print(cost)
print("The selected Paths and Payloads are: ")
for i in range(len(selected_weight)):
    print("Path: ",selected_path_s[i],selected_path_e[i])
    print("Payload Weight: ",selected_weight[i])

