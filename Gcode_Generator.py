from Preprocess import detect_lines
import numpy as np


class GCode:
    def __init__(self):
        '''
        
        gcode : List
            A list that storages gcodes lines
        Returns
        -------
        None.

        '''
        self.gcode=[]
        self.feed_rate=500
        self.line_number=0
    
    def g0(self,x=0,y=0,z=0):
        '''
        Add G0 command to "self.gcode"

        Parameters
        ----------
        x : Float, optional
            The default is 0.
        y : Float, optional
            The default is 0.
        z : Float, optional
            The default is 0.

        Returns
        -------
        None.

        '''
        g='G0'
        if x!=0:
            g+=' X'+str(x)
        if y!=0:
            g+=' Y'+str(y)
        if z!=0:
            g+=' Z'+str(z)
        g+=' ;N'+str(self.line_number)
        self.gcode+=[g]
        self.line_number+=1
        
    def g1(self,x=0,y=0,z=0):
        '''
        Add G1 command to "self.gcode"

        Parameters
        ----------
        x : Float, optional
            The default is 0.
        y : Float, optional
            The default is 0.
        z : Float, optional
            The default is 0.

        Returns
        -------
        None.

        '''
        g='G1'
        if x!=0:
            g+=' X'+str(x)
        if y!=0:
            g+=' Y'+str(y)
        if z!=0:
            g+=' Z'+str(z)
        g+=' F'+str(self.feed_rate)+' ;N'+str(self.line_number)
        self.gcode+=[g]
        self.line_number+=1

class GCode_Generator:
    def __init__(self):
        self.img_path='samples/01.jpg' #Source image path
        self.offset=(0,0) #Offset in X, Y in mm
        self.sheet_size=250 #Maximum Sheet size in mm
        self.Z_offset=-1 #Offset in Z in mm
        self.pen_up_delta_Z=2 #Distance of pen from sheet in  mm
        self.save_time_mode=True
        '''
        save_time_mode : if True the gcode generating algorithm 
        will work faster with skipping duplicated points
        '''
        self.save_path='Exported_gcode.gcode'
        
    def image_process(self):
        self.lines,self.img_size=detect_lines(self.img_path)
        print(self.img_size)
        self.scale_ratio=max(self.img_size)/self.sheet_size
        self.xm=self.img_size[0]/2
        self.ym=self.img_size[1]/2
        # self.scale_ratio=1

        
    def process_line(self):
        for i in range(len(self.lines)):
            line=self.lines[i]
            line=line.astype('float32')
            line[:,0]=-1*(line[:,0]-self.xm)/self.scale_ratio-self.offset[0]
            line[:,1]=(line[:,1]-self.ym)/self.scale_ratio-self.offset[1]
            self.lines[i]=line
          


    def extract_GCODE(self):
        gcode=GCode()
        up=self.pen_up_delta_Z+self.Z_offset
        down=self.Z_offset
        gcode.g0(z=up)
        for line in self.lines:
            skipping=False
            for c,point in enumerate(line):
                if c==0:
                    gcode.g0(x=line[0,0], y=line[0,1])
                    gcode.g0(z=down)
                else:
                    if self.save_time_mode:
                        if np.equal(point, line[:c-1]).all(axis=1).any():
                            if not skipping:
                                gcode.g0(z=up)
                            skipping=True
                            continue
                        if skipping:
                            gcode.g0(x=point[0], y=point[1])
                            gcode.g0(z=down)
                            skipping=False
                    gcode.g1(x=point[0], y=point[1], z=down)       
                  
            gcode.g0(z=up)
        self.gcode=gcode
          
        
    def run(self):
        '''
        Runnig the process
        for generating the gcode you just need to call this method

        Returns
        -------
        None.

        '''
        self.image_process()
        self.process_line()
        self.extract_GCODE()
        self.export()
        
    def export(self):
        '''
        Exporting Gcode to local file

        Returns
        -------
        None.

        '''
        gcode=''
        for i in self.gcode.gcode:
            gcode+=i+'\n'
        f = open(self.save_path, "w")
        f.write(gcode)
        f.close()
        
        

if __name__=='__main__':
    gg=GCode_Generator()
    gg.img_path='samples/01.jpg'
    gg.save_time_mode=True
    gg.run()

