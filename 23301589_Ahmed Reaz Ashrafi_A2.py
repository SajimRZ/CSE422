# %%
# Task 1
import random

# (width, height)
comp_size = {
    0 : [5,5], #ALU
    1 : [7,4], #Cache
    2 : [4,4], #Control Unit
    3 : [6,6], #Register File
    4 : [5,3], #Decoder
    5 : [5,5]  #Floating Unit
}

""" Register File → ALU
Control Unit → ALU
ALU → Cache
Register File → Floating Unit
Cache → Decoder
Decoder → Floating Unit """

connections = [
    [3, 0], [2, 0], [0, 1], [3, 5], [1, 4], [4, 5]
]

#random populations
def generatePopulation(pop_size,grid_size):
    population = []
    for i in range(pop_size):
        temp = [] 
        for j in range(len(comp_size.keys())):
            #generate a random (x,y)
            x = random.randrange(0,25)
            y = random.randrange(0,25)
            # reset (x,y) until 
            while x + comp_size[j][0] > grid_size or y + comp_size[j][1] > grid_size:
                x = random.randrange(0,25)
                y = random.randrange(0,25)
            temp.append([x,y]) #(x,y) of every component in one chromosome

        population.append(temp) 
    return population

#calculate population fitnesses
def fitnessTest(chrmsm):
    overlaps = 0 #track how many overlaps

    #setup for area calc
    xmin_list = []
    x_max_list = []
    ymin_list = []
    y_max_list = []

    for i in range(len(chrmsm)):
        
        # comp location to compare
        #keep data stored for area calc
        Ax_left = chrmsm[i][0]
        xmin_list.append(Ax_left)
        Ax_right = chrmsm[i][0] + comp_size[i][0]
        x_max_list.append(Ax_right)

        Ay_down = chrmsm[i][1]
        ymin_list.append(Ay_down)
        Ay_up = chrmsm[i][1] + comp_size[i][1]
        y_max_list.append(Ay_up)

        for j in range(i+1,len(chrmsm)):
            #every other comp location
            Bx_left = chrmsm[j][0]
            Bx_right = chrmsm[j][0] + comp_size[j][0]

            By_down = chrmsm[j][1]
            By_up = chrmsm[j][1] + comp_size[j][1]
            
            #checks overlapping
            if not(Ax_right <= Bx_left or Ax_left >= Bx_right or Ay_down >= By_up or Ay_up <= By_down):
                overlaps += 1
    #find min, max of x
    xmin = min(xmin_list)
    xmax = max(x_max_list)
    #find min, max of y
    ymin = min(ymin_list)
    ymax = max(y_max_list)

    area = (xmax - xmin) * (ymax - ymin) #calculate area = x * y
    
    # Wire Lemgth calculations
    dist = 0
    for i in connections:
        u,v = i
        u_center = [ chrmsm[u][0] + (comp_size[u][0]/2), chrmsm[u][1] + (comp_size[u][1]/2) ] 
        v_center = [ chrmsm[v][0] + (comp_size[v][0]/2), chrmsm[v][1] + (comp_size[v][1]/2) ]

        dist += ( (v_center[0] - u_center[0])**2 + (v_center[1] - u_center[1])**2 )**(1/2)
    
    penalty = 1000*overlaps + 5*dist + 3*area
    return [penalty, overlaps, dist, area]

# use parent to make children
def generate_children(population):
    children = []

    for i in range(pop_size):
        #pick two parents
        p1 = random.randint(0,len(population)-1)
        p2 = random.randint(0,len(population)-1)
        #p1 and p2 cant be same
        while p2 == p1:
            p2 = random.randint(0,len(population)-1)
    
        c1, c2 = single_point_crossingover(p1,p2)
        #mutation
        c1_mdex = random.randint(0, len(comp_size.keys())-1)
        c2_mdex = random.randint(0, len(comp_size.keys())-1)
        for j in range(len(comp_size.keys())):
            if j == c1_mdex:
                if random.random() < 0.08:
                    x = random.randrange(0,25)
                    y = random.randrange(0,25)
                    # reset (x,y) until 
                    while x + comp_size[j][0] > grid_size or y + comp_size[j][1] > grid_size:
                        x = random.randrange(0,25)
                        y = random.randrange(0,25)
                    c1[j] = [x,y]
            elif j == c2_mdex:
                if random.random() < 0.08:
                    x = random.randrange(0,25)
                    y = random.randrange(0,25)
                    # reset (x,y) until 
                    while x + comp_size[j][0] > grid_size or y + comp_size[j][1] > grid_size:
                        x = random.randrange(0,25)
                        y = random.randrange(0,25)
                    c2[j] = [x,y]
        children.append(c1)
        children.append(c2)
    return children

#Elitism + children to make a population for next loop  
def next_generation_prep(children,cur_gen):
    gen2 = []
    min1  = history[cur_gen][0]
    min2 = history[cur_gen][0]
    for i in range(len( history[cur_gen])):
        if history[cur_gen][i] < min1:
            min1 = history[cur_gen][i]
        if history[cur_gen][i] < min2 and history[cur_gen][i] > min1:
            min2 = history[cur_gen][i]
    
    gen2.append(min1[4])
    gen2.append(min2[4])

    for i in range(pop_size-2):
        a =  random.randint(0, len(comp_size.keys())-1-i)
        gen2.append(children[a])
        children.pop(a)
    
    return gen2
        
#size of population
pop_size = 6

#grid_size = input("Grid Size (one int value): ") #size of grid
grid_size = 25

#generate a random population for first loop
population = generatePopulation(pop_size,grid_size)
history = {}


#how many times loop will run
gens = 15

# Single point crossing over for children generation
def single_point_crossingover(p1,p2):
     #pick crossing over point
    rindx = random.randint(0, len(comp_size.keys())-2) #keep atleast one for crossing over
    #make children
    c1 = []
    c2 = []
    
    for j in range(len(comp_size.keys())):
        if j <= rindx:
            c1.append(population[p1][j])
            c2.append(population[p2][j])
        else:
            c1.append(population[p2][j])
            c2.append(population[p1][j])
    
    return [c1, c2]

#The main algotithm loop
def GenAlgo(population, cur_gen, gens, history):

    
    if cur_gen == gens:
        min_list = []  
        for i in history.keys():
            temp = min(history[i])
            min_list.append(temp)
        
        output = min(min_list)
        print(f'Best Fitness: {output[0]}')
        print(f'Total Wire length: {output[2]}')
        print(f'Total Bounding Box Area: {output[3]}')
        print(f'Total Overlaps: {output[1]}')
        print(f'Placement coordinates: {output[4]}')

        return output
    
    # check fitness and update history 
    for i in population:
        penalty, overlaps, dist, area = fitnessTest(i)
        if cur_gen not in history.keys():
            history[cur_gen] = [[penalty, overlaps, dist, area, i]]
        else:
            history[cur_gen].append([penalty, overlaps, dist, area, i])
    
    #generate children and pick next generation
    children = generate_children(population)
    gen2 = next_generation_prep(children,cur_gen)

    #loop in next generation
    return GenAlgo(gen2, cur_gen+1, gens, history)


output = GenAlgo(population, 0, gens, history)  
   


# %%
# Task 2
import random

def double_point_crossingover(p1,p2):
    #pick crossing over point
    rindx1 = random.randint(0, len(comp_size.keys())-3) #keep atleast two at end
    rindx2 = random.randint(rindx1, len(comp_size.keys())-2) #keep atleast one at end

    #make children
    c1 = []
    c2 = []
    
    for j in range(len(comp_size.keys())):
        if j <= rindx1:
            c1.append(population[p1][j])
            c2.append(population[p2][j])
        
        elif j > rindx1 and j <= rindx2:
            
            c1.append(population[p2][j])
            c2.append(population[p1][j])
        
        else:
            c1.append(population[p1][j])
            c2.append(population[p2][j])
    
    return [c1, c2]

##using double point instead of single point
def generate_children(population):
    children = []

    for i in range(pop_size):
        #pick two parents
        p1 = random.randint(0,len(population)-1)
        p2 = random.randint(0,len(population)-1)
        #p1 and p2 cant be same
        while p2 == p1:
            p2 = random.randint(0,len(population)-1)
    
        c1, c2 = double_point_crossingover(p1,p2) #using double point instead of single point
        #mutation
        c1_mdex = random.randint(0, len(comp_size.keys())-1)
        c2_mdex = random.randint(0, len(comp_size.keys())-1)
        for j in range(len(comp_size.keys())):
            if j == c1_mdex:
                if random.random() < 0.08:
                    x = random.randrange(0,25)
                    y = random.randrange(0,25)
                    # reset (x,y) until 
                    while x + comp_size[j][0] > grid_size or y + comp_size[j][1] > grid_size:
                        x = random.randrange(0,25)
                        y = random.randrange(0,25)
                    c1[j] = [x,y]
            elif j == c2_mdex:
                if random.random() < 0.08:
                    x = random.randrange(0,25)
                    y = random.randrange(0,25)
                    # reset (x,y) until 
                    while x + comp_size[j][0] > grid_size or y + comp_size[j][1] > grid_size:
                        x = random.randrange(0,25)
                        y = random.randrange(0,25)
                    c2[j] = [x,y]
        children.append(c1)
        children.append(c2)
    return children

#using double point instead of single point
def GenAlgo(population, cur_gen, gens, history):

    
    if cur_gen == gens:
        min_list = []  
        for i in history.keys():
            temp = min(history[i])
            min_list.append(temp)
        
        output = min(min_list)
        print(f'Best Fitness: {output[0]}')
        print(f'Total Wire length: {output[2]}')
        print(f'Total Bounding Box Area: {output[3]}')
        print(f'Total Overlaps: {output[1]}')
        print(f'Placement coordinates: {output[4]}')

        return output
    
    # check fitness and update history 
    for i in population:
        penalty, overlaps, dist, area = fitnessTest(i)
        if cur_gen not in history.keys():
            history[cur_gen] = [[penalty, overlaps, dist, area, i]]
        else:
            history[cur_gen].append([penalty, overlaps, dist, area, i])
    
    #generate children and pick next generation
    children = generate_children(population)
    gen2 = next_generation_prep(children,cur_gen)

    #loop in next generation
    return GenAlgo(gen2, cur_gen+1, gens, history)

population = generatePopulation(pop_size,grid_size)
history = {}

output = GenAlgo(population, 0, gens, history)  


