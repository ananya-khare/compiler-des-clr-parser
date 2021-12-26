from tabulate import tabulate
from collections import OrderedDict
import first_follow
from PIL import Image
import re
from first_follow import production_list,dfa_string, nt_list as ntl, t_list as tl
import time
import psutil
from collections import defaultdict
from graphviz import Digraph

nt_list, t_list=[], []

class State:
    _id=0
    def __init__(self, closure):
        self.closure=closure
        self.no=State._id
        State._id+=1

class Item(str):
    def __new__(cls, item, lookahead=list()):
        self=str.__new__(cls, item)
        self.lookahead=lookahead
        return self

    def __str__(self):
        return super(Item, self).__str__()+", "+'|'.join(self.lookahead)
        
######################################################################################################################
# depak kalal startsss
def closure(items):
    def exists(newitem, items):
        for i in items:
            if i==newitem and sorted(set(i.lookahead))==sorted(set(newitem.lookahead)):
                return True
        return False  
    global production_list
    while True:
        flag=0
        for i in items:             
            if i.index('.')==len(i)-1: continue
            Y=i.split('->')[1].split('.')[1][0]
            if i.index('.')+1<len(i)-1:
                lastr=list(first_follow.compute_first(i[i.index('.')+2])-set(chr(1013)))                
            else:
                lastr=i.lookahead           
            for prod in production_list:
                head, body=prod.split('->')                
                if head!=Y: continue                
                newitem=Item(Y+'->.'+body, lastr)
                if not exists(newitem, items):
                    items.append(newitem)
                    flag=1
        if flag==0: break
    return items

def goto(items, symbol):
    global production_list
    initial=[]
    for i in items:
        if i.index('.')==len(i)-1: continue
        head, body=i.split('->')
        seen, unseen=body.split('.')
        if unseen[0]==symbol and len(unseen) >= 1:
            initial.append(Item(head+'->'+seen+unseen[0]+'.'+unseen[1:], i.lookahead))
    return closure(initial)
# depak kalal Endsssss
######################################################################################################################




######################################################################################################################
# Kushagraaaaaaa startsss
def calc_states():
    def contains(states, t):
        for s in states:
            if len(s) != len(t): continue
            if sorted(s)==sorted(t):
                for i in range(len(s)):
                        if s[i].lookahead!=t[i].lookahead: break
                else: return True
        return False
    global production_list, nt_list, t_list
    head, body=production_list[0].split('->')
    states=[closure([Item(head+'->.'+body, ['$'])])]  
    while True:
        flag=0
        for s in states:
            for e in nt_list+t_list:
                t=goto(s, e)
                if t == [] or contains(states, t): continue
                states.append(t)
                flag=1
        if not flag: break
    return states 

def make_table(states):
    global nt_list, t_list
    
    def getstateno(t):
        for s in states:
            if len(s.closure) != len(t): continue

            if sorted(s.closure)==sorted(t):
                for i in range(len(s.closure)):
                        if s.closure[i].lookahead!=t[i].lookahead: break
                else: return s.no

        return -1

    def getprodno(closure):

        closure=''.join(closure).replace('.', '')
        return production_list.index(closure)

    SLR_Table=OrderedDict()
    
    for i in range(len(states)):
        states[i]=State(states[i])

    for s in states:
        SLR_Table[s.no]=OrderedDict()

        for item in s.closure:
            head, body=item.split('->')
            if body=='.': 
                for term in item.lookahead: 
                    if term not in SLR_Table[s.no].keys():
                        SLR_Table[s.no][term]={'r'+str(getprodno(item))}
                    else: SLR_Table[s.no][term]= {'r'+str(getprodno(item))}
                continue

            nextsym=body.split('.')[1]
            if nextsym=='':
                if getprodno(item)==0:
                    SLR_Table[s.no]['$']='accept'
                else:
                    for term in item.lookahead: 
                        if term not in SLR_Table[s.no].keys():
                            SLR_Table[s.no][term]={'r'+str(getprodno(item))}
                        else: SLR_Table[s.no][term]= {'r'+str(getprodno(item))}
                continue

            nextsym=nextsym[0]
            t=goto(s.closure, nextsym)
            if t != []: 
                if nextsym in t_list:
                    if nextsym not in SLR_Table[s.no].keys():
                        SLR_Table[s.no][nextsym]={'s'+str(getstateno(t))}
                    else: SLR_Table[s.no][nextsym]= {'s'+str(getstateno(t))}

                else: SLR_Table[s.no][nextsym] = str(getstateno(t))

    return SLR_Table

# Kushagraaaa Endsssss
######################################################################################################################


######################################################################################################################
# depak kalal startsss
def augment_grammar():

    for i in range(ord('Z'), ord('A')-1, -1):
        if chr(i) not in nt_list:
            print(production_list)
            start_prod=production_list[0]
            production_list.insert(0, chr(i)+'->'+start_prod.split('->')[0]) 
            return production_list

# depak kalal Endsssss
######################################################################################################################



#generate DFA from items generated after LR(0) items boiler plate codee
            
def generate_dfa():
    
    im = Image.open("genratedDFA.png")
    
    process_list = []
    for proc in psutil.process_iter():
        process_list.append(proc)
 
    im.show()
    
    # display image for 10 seconds
    time.sleep(5)
    
    
    for proc in psutil.process_iter():
        if not proc in process_list:
            proc.kill()     

#boiler plate codee for dfa ui


#############################################################################################################################
# Aadarshhhhhhh Startsssssss
def main():

    global production_list, ntl, nt_list, tl, t_list  
    
    table=[]
    c=0
    first_follow.main()
    
    for i in range(len(production_list)):
        c+=1
    print("\tFIRST AND FOLLOW OF NON-TERMINALS \n")
    
    for nt in ntl:
        first_follow.compute_first(nt)
        first_follow.compute_follow(nt)
        table.append([nt,first_follow.get_first(nt),first_follow.get_follow(nt)])   
    print(tabulate(table,headers=["VARIABLES","FIRST  ","FOLLOW "],tablefmt="pretty"))    
    

    print("\nAugmented Grammar- ")
    print(augment_grammar())
    print('\n')
    nt_list=list(ntl.keys())
    t_list=list(tl.keys()) + ['$']

    j=calc_states()
    #generate_dfa()
    ctr=0
    for s in j:
        print("Item{}:".format(ctr))
        #dfa generation process collecting states here
        #states_array.append({"Item{}".format(ctr):s,"arrows":[[x for x in re.split("->",prod)][1] for prod in s]})
        
        for i in s:
            print("\t", i)
        ctr+=1
    generate_dfa()   
        
        # dfa creation left

    table=make_table(j)
    print('_____________________________________________________________________')
    print("\nProductions are numbered as follows: ")
    for i in range(c):
        print(i+1, production_list[i+1])
    print("\n\t CLR(1) Parsing TABLE")
    print('\t-----------------------\n')
    sym_list = nt_list + t_list
    sr, rr=0, 0
    print('_____________________________________________________________________')
    print('      \t|  ','\t'.join([" " for i in range(int(len(nt_list)))]),"    "," | ",''.join([" " for i in range(int(len(t_list)))]),"         ",'\t\t')
    print('      \t|  ','\t'.join([" " for i in range(int(len(nt_list)))]),"Goto"," | ",''.join([" " for i in range(int(len(t_list)))])," Action ",'\t\t')
    print('      \t|  ','\t'.join([" " for i in range(int(len(nt_list)))]),"    "," | ",''.join([" " for i in range(int(len(t_list)))]),"         ",'\t\t')
    print('_____________________________________________________________________')
    
    print('States\t|  ','\t|  '.join(sym_list),'\t\t')
    print('---------------------------------------------------------------------')
    for i, j in table.items():  
        print(i, "\t|  ", '\t|  '.join(list(j.get(sym,' ') if type(j.get(sym))in (str , None) else next(iter(j.get(sym,' ')))  for sym in sym_list)),'\t\t')
        s, r=0, 0

        for p in j.values():
            if p!='accept' and len(p)>1:
                p=list(p)
                if('r' in p[0]): r+=1
                else: s+=1
                if('r' in p[1]): r+=1
                else: s+=1      
        if r>0 and s>0: sr+=1
        elif r>0: rr+=1
    print('_____________________________________________________________________')
    print("\n", sr, "s/r conflicts and", rr, "r/r conflicts")
    print('_____________________________________________________________________')
    print("Enter the string to be parsed- ")
    Input=input()+'$'
    print("Input string- ",Input)
    try:
        stack=['0']
        a=list(table.items())
        '''print(a[int(stack[-1])][1][Input[0]])
        b=list(a[int(stack[-1])][1][Input[0]])
        print(b[0][0])
        print(a[0][1]["S"])'''
##        print("productions\t:",production_list)
        print("\n\t-------------")
        print('Stack- ',*stack,sep=" | ")
        print("\t-------------")
        while(len(Input)!=0):
            b=list(a[int(stack[-1])][1][Input[0]])
            if(b[0][0]=="s" ):
                #s=Input[0]+b[0][1:]
                stack.append(Input[0])
                stack.append(b[0][1:])
                Input=Input[1:]
                print("\nString-  ",*Input)
                print("\t--------------------------")
                print('Stack- ',*stack,sep=" | ")
                print("\t--------------------------")
            elif(b[0][0]=="r" ):
                s=int(b[0][1:])
                #print(len(production_list),s)
                l=len(production_list[s])-3
                #print(l)
                prod=production_list[s]
                l*=2
                l=len(stack)-l
                stack=stack[:l]
                s=a[int(stack[-1])][1][prod[0]]
                #print(s,b)
                stack+=list(prod[0])
                stack.append(s)
                print("\nString-  ",*Input)
                print("\t--------------------------")
                print('Stack- ',*stack,sep=" | ")
                print("\t--------------------------")
               
            elif(b[0][0]=="a"):
                print("\n\tString Accepted\n")
                break
    except:
        print('\n\tString INCORRECT for given Grammar!\n')
    return 


if __name__=="__main__":
    main()
# Aadarshhhhhhh Endsssssssssssssssss
#############################################################################################################################