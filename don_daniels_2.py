# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 13:17:58 2017
reads file into list for cooccurence measurement of features
@author: Wolfgang
"""
# first set files
#fname = open('C:/Users/Wolfgang/Dropbox/Sogeram Raw Files/first set/lex.csv', 'r')
#foutput = open('C:/Users/Wolfgang/Dropbox/Sogeram Raw Files/first set/lex_out.csv', 'w')
#fname = open('C:/Users/Wolfgang/Dropbox/Sogeram Raw Files/first set/morph.csv', 'r')
#foutput = open('C:/Users/Wolfgang/Dropbox/Sogeram Raw Files/first set/morph_out.csv', 'w')
#fname = open('C:/Users/Wolfgang/Dropbox/Sogeram Raw Files/first set/phon.csv', 'r')
#foutput = open('C:/Users/Wolfgang/Dropbox/Sogeram Raw Files/first set/phon_out.csv', 'w')
#fname = open('C:/Users/Wolfgang/Dropbox/Sogeram Raw Files/first set/syn.csv', 'r')
#foutput = open('C:/Users/Wolfgang/Dropbox/Sogeram Raw Files/first set/syn_out.csv', 'w')

# second set files
#fname = open('C:/Users/Wolfgang/Dropbox/Sogeram Raw Files/second set/distr.csv', 'r')
#foutput = open('C:/Users/Wolfgang/Dropbox/Sogeram Raw Files/second set/distr_out.csv', 'w')
#fname = open('C:/Users/Wolfgang/Dropbox/Sogeram Raw Files/second set/form.csv', 'r')
#foutput = open('C:/Users/Wolfgang/Dropbox/Sogeram Raw Files/second set/form_out.csv', 'w')
fname = open('C:/Users/Wolfgang/Dropbox/Sogeram Raw Files/second set/sem.csv', 'r')
foutput = open('C:/Users/Wolfgang/Dropbox/Sogeram Raw Files/second set/sem_out.csv', 'w')

# main file
#fname = open('C:/Users/Wolfgang/Dropbox/Sogeram Raw Files/Sogeram innovations_with xs_w.csv', 'r')
#foutput = open('C:/Users/Wolfgang/Dropbox/Sogeram Raw Files/Sogeram innovations_with xs_w_out.csv', 'w')


# for each type each line in the file is written to protocol incl. evaluation
protocol = open('C:/Users/wolfgang/Documents/Australien/Don/output/protocol.csv', 'w')
lineList = []   # list of all lines in the file
typeDict = {}   # all DIFFERENT types as key and their values        
sigmaList = []  # to find a min and max sigma value
resultDict = {} # dict to write on output
foutput.write("languageGroup;freqency;p-value;q-value;k-value;sigma;sigma_norm\n")
    
class Line:
    """
    each line in the input file -> instance of Line class 
    """
    
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
        
    def allInGroup(self, typeList):
        """
        param typeList = list of languages the instance is compared to
        return True: all languages from typeList are in instance
        """
        groupList = groupToGroupList(self.languageGroup('1'))
        allIn = True
        for x in typeList:
            if x not in groupList:
                allIn = False
        return allIn
        
        
    def oneInGroup(self, typeList):
        """
        param typeList = list of languages the instance is compared to
        return True: One of instance list is in typeList
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
    
    # only x free lines are counted as group
    if len(instance.languageGroup("x")) == 0:
        
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
    
    # write the type to protocol
    protocol.write(k + "\n")
    # iterate over lines
    for line in lineList[1:]:
       
        # write the line id to proptocol
        protocol.write("\t" + line.split(",")[0] + "\n")
        
        # create Line instance
        instance = makeInstance(line)
                
        allIn = instance.allInGroup(kList)       # all of type in instance
        oneIn = instance.oneInGroup(kList)       # one of instance is in type
        oneOut = instance.oneOutOfGroup(kList)   # one of instance is out of type
        zeroInGroup = instance.zeroInGroup(kList)# one of type is not in instance
        
        # p value: supporting the type
        if allIn:
            resultDict[k][1] += 1
            #print "p line: " + instance.languageGroup("1") + " type: " + str(kList)
            # write found supporting lines p to protocol            
            protocol.write(" p line: " + instance.languageGroup("1") + " type: " + str(kList) + "\n")
        
        # q value: unsupports the type
        if oneIn and oneOut and zeroInGroup:
            resultDict[k][2] += 1
            #print "q line: " + instance.languageGroup("1") + " type: " + str(kList)
            # write found unsupporting lines q to protocol
            protocol.write(" q line: " + instance.languageGroup("1") + " type: " + str(kList) + "\n")
            
        
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
    
    foutput.write(k + ";" 
                 + str(v[0]) + ";" 
                 + str(v[1]) + ";" 
                 + str(v[2]) + ";"
                 + str(v[3]) + ";"
                 + str(v[4]) + ";"
                 + str(v[5]) + "\n")

fname.close()
foutput.close()
protocol.close()
