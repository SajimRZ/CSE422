# %%
# TASK 1

pool = ['A','T','C','G']
target = 'GCAT'
id = '2 3 3 0 1 5 8 9'

def minimax(pool, target, gene, alpha, beta, turn):
    #calculate score 
    def Utility(gene,target,id):
        id = id.split(' ')
        #last digites of id
        weight = id[len(id)-len(target):]
        total = 0
        #ascii distance * weight
        for i in range(len(gene)):
            total += int(weight[i]) * abs( ord(gene[i]) - ord(target[i]) )

        return -total

    #base case -> pool empty
    if not pool:
        return [Utility(gene,target,id), gene] #calculate score, return sequence
    #max turn
    if turn == 'max':
        #start all -infinity
        max_val = float('-inf')
        sequence = ''

        #all posible children combination
        for i in range(len(pool)):
            new_pool = pool[:i] + pool[i+1:] #pool - cromosome chosen
            cur_gene = gene+pool[i]
            val, seq = minimax(new_pool, target, cur_gene, alpha, beta, 'min') #goes down tree until base
            
            #if update sequence only when better route is found
            if val > max_val:
                max_val = val
                sequence = seq
            #when beta < alphga stop checking
            alpha = max(alpha, val) 
            if beta <= alpha:
                break

        return [max_val, sequence]
    
    #same same but different
    elif turn == 'min':
        min_val = float('inf')
        sequence = ''
        for i in range(len(pool)):
            new_pool = pool[:i] + pool[i+1:]
            cur_gene = gene+pool[i]
            val, seq = minimax(new_pool, target, cur_gene, alpha, beta, 'max')

            if val < min_val:
                min_val = val
                sequence = seq

            beta = min(beta, val)

            if beta <= alpha:
                break

        return [min_val, sequence]

score, sequence = minimax(pool, target, '', float('-inf'), float('inf'), 'max')

print(f'Best gene sequence generated: {sequence}')
print(f'Utility Score: {score}')





# %%
# TASK 2
pool = ['A','T','C','G']
target = 'GCAT'
id = '2 3 3 0 1 5 8 9'



def compare(pool, target, id):
    

    def minimaxgold(pool, target, gene, alpha, beta, id, turn, boost):

        def UtilityGold(gene,target, id):
            id = id.split()
            weight = id[len(id)-len(target):]
            weight = list(map(int, weight))
            
            if boost == True:
                top = int(id[0] + id[1])
                for i in range(len(gene)):
                    if gene[i] == 'S':
                        for j in range(len(weight)):
                            if j >= i:
                                weight[j] = (top/100) * weight[j]
                        break          
            total = 0
            
            for i in range(len(gene)):
                if i < len(target):  
                    total += weight[i] * abs( ord(gene[i]) - ord(target[i]) )
                else:
                    total += abs(ord(gene[i]))
            return -total
        
        if not pool:
            return [UtilityGold(gene, target, id), gene]

        if turn == 'max':
            max_val = float('-inf')
            sequence = ''

            for i in range(len(pool)):
                new_pool = pool[:i] + pool[i+1:] 
                cur_gene = gene+pool[i]
                if pool[i] == 'S':
                    boost = True
                
                val, seq = minimaxgold(new_pool, target, cur_gene, alpha, beta, id, 'min', boost)
                if val > max_val:
                    max_val = val
                    sequence = seq
                #when beta < alphga stop checking
                alpha = max(alpha, val) 
                

            return [max_val, sequence]
        
        #same same but different
        elif turn == 'min':
            min_val = float('inf')
            sequence = ''
            for i in range(len(pool)):
                new_pool = pool[:i] + pool[i+1:]
                cur_gene = gene+pool[i]
                val, seq = minimaxgold(new_pool, target, cur_gene, alpha, beta, id, 'max',boost)

                if val < min_val:
                    min_val = val
                    sequence = seq

                beta = min(beta, val)

                

            return [min_val, sequence]

    
    score, sequence = minimax(pool, target, '', float('-inf'), float('inf'), 'max')
    
    pool.append('S')
    boost = False

    gscore, gseq = minimaxgold(pool, target, '', float('-inf'), float('inf'), id, 'max', boost)

    if gscore > score:
        print('YES')
    else:
        print('NO')
    print(f'Best gene sequence generated: {gseq}')
    print(f'Utility Score: {gscore}')

compare(pool, target, id)



