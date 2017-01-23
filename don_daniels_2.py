# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 13:17:58 2017
reads file into list for cooccurence measurement of features
@author: Wolfgang
"""
#fname = open('C:/Users/wolfgang/Documents/Australien/Don/don.txt', 'r')
#foutput = open('C:/Users/wolfgang/Documents/Australien/Don/don_out.txt', 'w')
#fname = open('C:/Users/wolfgang/Documents/Australien/Don/raw files/Sogeram innovations_without irr sound change.txt', 'r')
#foutput = open('C:/Users/wolfgang/Documents/Australien/Don/output/Sogeram innovations_without irr sound change_o.txt', 'w')
fname = open('C:/Users/wolfgang/Documents/Australien/Don/raw files/Sogeram innovations_without prt sound change.csv', 'r')
#foutput = open('C:/Users/wolfgang/Documents/Australien/Don/output/Sogeram innovations_without prt sound change_o.txt', 'w')
foutput2 = open('C:/Users/wolfgang/Documents/Australien/Don/output/Sogeram innovations_without prt sound change_o2.txt', 'w')
#fname = open('C:/Users/wolfgang/Documents/Australien/Don/raw files/Sogeram innovations_without xs.txt', 'r')
#foutput = open('C:/Users/wolfgang/Documents/Australien/Don/output/Sogeram innovations_without xs_o.txt', 'w')
#fname = open('C:/Users/wolfgang/Documents/Australien/Don/raw files/Sogeram innovations_with xs.txt', 'r')
#foutput = open('C:/Users/wolfgang/Documents/Australien/Don/output/Sogeram innovations_with xs_o.txt', 'w')

lineList = []   # list of all lines in the file
typeDict = {}   # all DIFFERENT types as key and their values        
sigmaList = []  # to find a min and max sigma value
resultDict = {} # dict to write on output
foutput2.write("languageGroup;freuqency;p-value;q-value;k-value;sigma;sigma_norm\n")
    
class Line: # each line in the input file -> instance of Line class 
    def __init__(self, id, name, typ, Mnd, Nen, Mnt, Apa, Mum, Sir, Mag, Ais, Kur, Gaj):
        self.name = name        
        self.id = id
        self.typ = typ        
        self.mnd = [Mnd, "Mnd"]
        self.nen = [Nen, "Nen"]
        self.mnt = [Mnt, "Mnt"]
        self.apa = [Apa, "Apa"]
        self.mum = [Mum, "Mum"]
        self.sir = [Sir, "Sir"]
        self.mag = [Mag, "Mag"]
        self.ais = [Ais, "Ais"]
        self.kur = [Kur, "Kur"]
        self.gaj = [Gaj, "Gaj"]
    
    
    def languageGroup(self, variable):
        """
        param variable: 1 feature in language
                        0 feature not in language 
                        x unknown if in or not in language
        return string of language glosses
        """
        group = ""
        for x in [self.mnd, 
                  self.nen, 
                  self.mnt, 
                  self.apa, 
                  self.mum,
                  self.sir, 
                  self.mag,
                  self.ais,
                  self.kur,
                  self.gaj]:
            if x[0] == variable:
                group = group + x[1]
        return group
        
        
    def oneInGroup(self, typeList):
        """
        param typeList = list of languages the instance is compared to
        return True: One of instance list is in typeList
        True for ABC in line ADE, AD; False for ABC in line DEF, EF
        """
        groupList = groupToGroupList(self.languageGroup('1'))
            
        oneIn = False
        for x in groupList:
            if x in typeList:
                oneIn = True
        return oneIn
       
       
    def oneOutOfGroup(self, typeList):
        """
        param typeList = list of languages the instance is compared to
        return True: One of instance list is not in typeList
        True for ABC in line AB, ABD; False for ABC in line ABC, ABCD
        """
        groupList = groupToGroupList(self.languageGroup('1'))
        oneOut = False
        for x in groupList:
            if x not in typeList:
                oneOut = True
        return oneOut
    
        
    def zeroInGroup(self, typeList):
        """
        param typeList = list of languages the instance is compared to
        return True: One of instance 0-list is in typeList
        True for ABC in line ABD
        False for ABC in line AB, ABC
        """
        groupList = groupToGroupList(self.languageGroup('0'))
        
        oneZero = False
        for x in groupList:
            if x in typeList:
                oneZero = True
        return oneZero
                   

def groupToGroupList(group):
    """
    param group: String of three letter languages glosses
    return groupList: list of three letter glosses
    """
    groupList = []
    for i in range(0, len(group), 3):
        groupList.append(group[i:i+3])
    return groupList


def makeInstance(line):
    """
    param line: each line from list of lines
    return instance of Line class
    """    
    
    splitLine = line.split(",")
    
    instance = Line(splitLine[1][1:-1],        # idNr
                    "id" + splitLine[1][1:-1], # name
                    splitLine[3][1:-1],        # typ
                    splitLine[6][1:-1],        # Mnd
                    splitLine[7][1:-1],        # Nen
                    splitLine[8][1:-1],        # Mnt
                    splitLine[9][1:-1],        # Apa
                    splitLine[10][1:-1],       # Mum
                    splitLine[11][1:-1],       # Sir
                    splitLine[12][1:-1],       # Mag
                    splitLine[13][1:-1],       # Ais
                    splitLine[14][1:-1],       # Kur
                    splitLine[15][1:-1])       # Gaj
    return instance


# read all lines in list
for line in fname:
    lineList.append(line)


# add all different types to typeDict
# count how often they occure  
for line in lineList[1:]:
    instance = makeInstance(line)
    
    if instance.languageGroup("1") in typeDict:
        typeDict[instance.languageGroup("1")] += 1
    else:
        typeDict[instance.languageGroup("1")] = 1


# calculate p and q values
for k, v in typeDict.iteritems():
   
    # create list of languages    
    kList = groupToGroupList(k)
    
    # frequency, p-value, q-value, k-value, sigma, sigma_normalized
    resultDict[k] = [v, 0, 0, 0, 0, 0]
    
    # iterate over lines
    for line in lineList[1:]:
        
        # create Line instance
        instance = makeInstance(line)
                
        oneIn = instance.oneInGroup(kList)       # one of instance is in type
        oneOut = instance.oneOutOfGroup(kList)   # one of instance is out of type
        zeroInGroup = instance.zeroInGroup(kList)# one of type is not in instance
        
        # p value: supporting the type
        if oneIn and not zeroInGroup:
            resultDict[k][1] += 1
            print "p line: " + instance.languageGroup("1") + " type: " + str(kList)
        
        # q value: unsupports the type
        if oneIn and oneOut and zeroInGroup:
            resultDict[k][2] += 1
            print "q line: " + instance.languageGroup("1") + " type: " + str(kList)


# calculate k-value and sigma
for k, v in resultDict.iteritems():
    
    # calculate k-value
    resultDict[k][3] = float(resultDict[k][1]) / (resultDict[k][1] 
                                                + resultDict[k][2])
    
    # calculate sigma value                                           
    resultDict[k][4] = resultDict[k][3] * resultDict[k][0]
    sigmaList.append(resultDict[k][4])


# for normilaization of sigma
sigmaMin = min(sigmaList)
sigmaMax = max(sigmaList)
    
    
# sigma_norm 
for k, v in resultDict.iteritems():
    
    #calculate sigma norm
    resultDict[k][5] =  (resultDict[k][4] 
                               - sigmaMin) / (sigmaMax 
                                              - sigmaMin)
    
    foutput2.write(k + ";" 
                 + str(v[0]) + ";" 
                 + str(v[1]) + ";" 
                 + str(v[2]) + ";"
                 + str(v[3]) + ";"
                 + str(v[4]) + ";"
                 + str(v[5]) + "\n")

foutput2.close()