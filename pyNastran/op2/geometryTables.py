import os
import sys
import struct
from struct import unpack

class GeometryTables(object):

    def readTable_Geom1(self):
        print "--------GEOM 1---------"
        word = self.readTableName(rewind=False) # GEOM1
        print "*tableName = |%r|" %(word)

        self.readMarkers([-1,7])
        fields = self.readIntBlock()
        print "fields = ",fields

        self.readMarkers([-2,1,0]) # 2
        bufferWords = self.getMarker()
        print "bufferWords = ",bufferWords,bufferWords*4
        word = self.readStringBlock()

        self.readMarkers([-3,1,0])
        marker = self.getMarker() # 35,315,1571
        print "marker = ",marker
        #self.printTableCode(marker)
        
        ints = self.readIntBlock()
        #print "*ints = ",ints, len(ints)

        #while ints:  ## @todo is this correct???
        #    coord1 = ints[:6]
        #    ints = ints[6:]
        #    print "coord1 = ",coord1

        self.readMarkers([-4,1,0])  #3
        bufferWords = self.getMarker()
        print "bufferWords = ",bufferWords,bufferWords*4
        
        if bufferWords==3:
            print "maybe a buffer block..."
            ints = self.readIntBlock() # buffer block...        
            print "  **ints = ",ints, len(ints)
            bufferSize = ints[0]
        
        self.printSection(100)
        #ints = self.readIntBlock()
        #print "*ints = ",ints, len(ints)

        #assert len(ints)==bufferWords,'len(ints)=%s bufferWords=%s' %(len(ints),bufferWords)
        #print "*ints = ",ints

        self.readMarkers([-5,1,0])
        markerA = self.getMarker('A')
        markerB = self.getMarker('B')
        if [markerA,markerB]==[0,2]:
            self.n-=24
            self.op2.seek(self.n)
            return
        print "markerA=%s  markerB=%s" %(markerA,markerB)
        #print "bufferWords = ",bufferWords,bufferWords*4
        self.printSection(100)
        sys.exit('stopping on geom 1')


    def readTable_Geom2(self):
        word = self.readTableName(rewind=False) # GEOM2
        print "tableName = |%r|" %(word)

        self.readMarkers([-1,7])
        ints = self.readIntBlock()
        print "*ints = ",ints

        self.readMarkers([-2,1,0]) #2
        bufferWords = self.getMarker()
        print "bufferWords = ",bufferWords,bufferWords*4
        word = self.readStringBlock()
        #print "word = |%r|" %(word)

        self.readMarkers([-3,1,0]) # 17
        bufferWords = self.getMarker()
        print "bufferWords = ",bufferWords,bufferWords*4

        #marker = self.getMarker() # 17
        #print "marker = ",marker
        #self.printTableCode(marker)
        ints = self.readIntBlock()  ## @todo do i need this...
        #print "*ints = ",ints

        self.readMarkers([-4,1,0]) # 3
        bufferWords = self.getMarker()
        print "bufferWords = ",bufferWords,bufferWords*4
        ints = self.readIntBlock()
        #print "*ints = ",ints
        #assert len(ints)==37
        
        # these sections arent always in the op2...
        if self.isTableDone([-5,1]):
            print "couldnt find table 5 in GEOM2..."
            return
        #print "tell = ",self.op2.tell(),self.n

        self.readMarkers([-5,1,0])
        if self.checkForGeom3():
            return

        bufferWords = self.getMarker()  # 31
        print "bufferWords = ",bufferWords,bufferWords*4
        ints = self.readIntBlock()
        print "*ints = ",ints

        #ints = self.readIntBlock()  ## @todo  need this for large problems....
        #print "*ints = ",ints
        
        #if self.isTableDone([-6,1]):
        #    print "couldnt find table 6 in GEOM2..."
        #    return

        self.readMarkers([-6,1,0])
        bufferWords = self.getMarker()  # 31
        ints = self.readIntBlock()

        iTable = -7
        while 1:  ## @todo could this cause an infinite loop...i dont this so...
            self.readMarkers([iTable,1,0])

            if self.checkForGeom3():
                return
            bufferWords = self.getMarker()
            ints = self.readIntBlock()

            #self.printSection(100)
            iTable -= 1
        ###

        
        self.printSection(100)
        sys.exit('end block of geom2...this should never happen...')


    def checkForGeom3(self):
        foundTable = False
        word = self.readTableName(rewind=True,stopOnFailure=False) # GEOM2
        if word == 'GEOM3':
            foundTable = True
        print "geom3word = ",word
        return foundTable

    def readTable_Geom3(self):
        ## GEOM3
        word = self.readTableName(rewind=False) # GEOM3
        print "tableName = |%r|" %(word)

        self.readMarkers([-1,7])
        ints = self.readIntBlock()
        print "*ints = ",ints

        self.readMarkers([-2,1,0])
        bufferWords = self.getMarker() # 2
        print "bufferWords = ",bufferWords,bufferWords*4
        word = self.readStringBlock()
        print "word = |%r|" %(word)

        self.readMarkers([-3,1,0]) # 24
        bufferWords = self.getMarker()
        #print "bufferWords = ",bufferWords,bufferWords*4
        #self.printSection(4*187)
        ints = self.readIntBlock()
        print "ints = ",ints
        #self.skip(4*26)
        

        #self.printSection(4*30)
        #self.readMarkers([-4,1,0]) # 9
        #bufferWords = self.getMarker()
        #print "bufferWords = ",bufferWords,bufferWords*4
        #ints = self.readIntBlock()
        #print "4,-1,0,ints = ",ints
        #self.skip(4*11)


        data = self.readTableData([-4,1,0],'GEOM3')
        data = self.readTableData([-5,1,0],'GEOM3')
        print "time for block section 6..."
        
        self.readMarkers([-6,1,0])
        #assert self.op2.tell()==1488,self.op2.tell()
        

    def readTableData(self,markers,tableName):
        self.readMarkers(markers,tableName) # 3
        bufferWords = self.getMarker()
        print "bufferWords = ",bufferWords,bufferWords*4
        self.printSection(80)
        data = self.readBlock()
        return data

    def readTable_Geom4(self):
        # GEOM4
        word = self.readTableName(rewind=False) # GEOM4
        print "tableName = |%r|" %(word)

        self.readMarkers([-1,7])
        ints = self.readIntBlock()
        print "*ints = ",ints

        self.readMarkers([-2,1,0]) # 2
        bufferWords = self.getMarker()
        print "bufferWords = ",bufferWords,bufferWords*4
        word = self.readStringBlock()
        print "word = |%r|" %(word)

        self.readMarkers([-3,1,0]) # 9
        bufferWords = self.getMarker()
        print "bufferWords = ",bufferWords,bufferWords*4
        ints = self.readIntBlock()
        print "*ints = ",ints

        self.readMarkers([-4,1,0]) # 6
        bufferWords = self.getMarker()
        print "bufferWords = ",bufferWords,bufferWords*4
        ints = self.readIntBlock()
        print "*ints = ",ints

        self.readMarkers([-5,1,0]) # 3
        bufferWords = self.getMarker()
        print "bufferWords = ",bufferWords,bufferWords*4
        ints = self.readIntBlock()
        print "*ints = ",ints

        self.readMarkers([-6,1,0])
        print "------------"

    def readTable_EPT(self):
        # EPT
        word = self.readTableName(rewind=False) # EPT
        print "word = |%r|" %(word)

        self.readMarkers([-1,7])
        ints = self.readIntBlock()
        print "*ints = ",ints

        self.readMarkers([-2,1,0]) # 2
        bufferWords = self.getMarker()
        print "bufferWords = ",bufferWords,bufferWords*4
        print "------------"
        word = self.readStringBlock()
        print "word = |%r|" %(word)

        self.readMarkers([-3,1,0]) # 14
        bufferWords = self.getMarker()
        print "bufferWords = ",bufferWords,bufferWords*4
        self.skip(4*16)

        self.readMarkers([-4,1,0]) # 3
        bufferWords = self.getMarker()
        print "bufferWords = ",bufferWords,bufferWords*4
        ints = self.readIntBlock()
        print "*ints = ",ints

        print "------------"
        self.readMarkers([-5,1,0])

    def readTable_MPTS(self):
        ## MPTS
        word = self.readTableName(rewind=False) # MPTS
        print "word = |%r|" %(word)

        self.readMarkers([-1,7])
        ints = self.readIntBlock()
        print "*ints = ",ints

        self.readMarkers([-2,1,0]) # 2
        bufferWords = self.getMarker()
        print "bufferWords = ",bufferWords,bufferWords*4

        print "------------"
        word = self.readStringBlock()
        print "word = |%r|" %(word)

        self.readMarkers([-3,1,0]) # 15
        bufferWords = self.getMarker()
        print "bufferWords = ",bufferWords,bufferWords*4
        ints = self.readIntBlock()
        print "*ints = ",ints

        self.readMarkers([-4,1,0]) # 3
        bufferWords = self.getMarker()
        print "bufferWords = ",bufferWords,bufferWords*4
        ints = self.readIntBlock()
        print "*ints = ",ints

        self.readMarkers([-5,1,0])
        print "------------"
        assert self.op2.tell()==2692,self.op2.tell()


