"""
Plugin name : CurlSmoke
Copyright: 
Written for CINEMA 4D R18.000

Modified Date: 07/02/2017
"""
import os
import sys
import c4d
from c4d import plugins, utils, bitmaps, gui
from c4d.utils import noise
# Be sure to use a unique ID obtained from www.plugincafe.com
# 1000001-1000010
PLUGIN_ID = 1038795


class CurlSmoke(plugins.ObjectData):
    


    """docstring for CurlSmoke"""
    
   

    def Init(self, op):
        
        self.InitAttr(op, float, [c4d.SPEED])
        
        self.InitAttr(op, float, [c4d.NOISESCALE])
        self.InitAttr(op, float, [c4d.DISP])





        self.speed = op[c4d.SPEED] = 1.0
        
        self.noise_offsets = c4d.Vector(0,150,600)
        self.offset = c4d.Vector(0)
        self.noiseScale = op[c4d.NOISESCALE] =  5.0
        self.disp = op[c4d.DISP]= 20.0

        


       

        return True


    
    def get_noise_val(self,x,y,z,axis):
        
        pos = c4d.Vector(x,y,z)
        noise_scale = self.noiseScale * 100.0
        return c4d.utils.noise.SNoise((pos+self.noise_offsets[axis]) / noise_scale, self.doc.GetTime().Get() * self.speed )
        

    
    def curl(self,pos):


        amplitude = 10 * self.speed
        disp = self.disp

        offset = c4d.Vector(0)
        #delta = 0.5/(disp)
        #delta = 500.0
        x = pos.x
        y = pos.y
        z = pos.z
        xpos = x + disp
        xneg = x - disp
        ypos = y + disp
        yneg = y - disp
        zpos = z + disp
        zneg = z - disp
        
        #nxpos = self.get_noise_val(xpos,y,z,0)
        #nxneg = self.get_noise_val(xneg,y,z,0)
        #nypos = self.get_noise_val(x,ypos,z,1)
        #nyneg = self.get_noise_val(x,yneg,z,1)
        #nzpos = self.get_noise_val(x,y,zpos,2)
        #nzneg = self.get_noise_val(x,y,zneg,2)
              
        offset.x = ((self.get_noise_val(x,ypos,z,2) - self.get_noise_val(x,yneg,z,2)) - (self.get_noise_val(x,y,zpos,1) - self.get_noise_val(x,y,zneg,1))) 
        offset.y = ((self.get_noise_val(x,y,zpos,0) - self.get_noise_val(x,y,zneg,0)) - (self.get_noise_val(xpos,y,z,2) - self.get_noise_val(xneg,y,z,2))) 
        offset.z = ((self.get_noise_val(xpos,y,z,1) - self.get_noise_val(xneg,y,z,1)) - (self.get_noise_val(x,ypos,z,0) - self.get_noise_val(x,yneg,z,0))) 
        
        #offset.x  = nypos - nyneg - nzpos + nzneg        
        #offset.y  = nzpos - nzneg - nxpos + nxneg
        #offset.z  = nxpos - nxneg - nypos + nyneg


        #offset *= delta
        offset.Normalize()
        return offset / 2.0*disp 
    
    def ModifyParticles(self, op, pp, ss, pcnt, diff):
        self.doc = op.GetDocument()
        self.speed = op.GetParameter(c4d.SPEED, c4d.DESCFLAGS_GET_0)
        #self.noiseoffsets = op.GetParameter(c4d.CURL_NOISE_OFFSET, c4d.DESCFLAGS_GET_0)
        #self.posOffset  = op.GetParameter(c4d.POS_OFFSET, c4d.DESCFLAGS_GET_0)
        self.noiseScale = op.GetParameter(c4d.NOISESCALE, c4d.DESCFLAGS_GET_0) 
        self.disp = op.GetParameter(c4d.DISP, c4d.DESCFLAGS_GET_0) 
        


        for i in xrange(pcnt):
            if ( not (pp[i].bits & c4d.PARTICLEFLAGS_VISIBLE)):
                continue

            #ss[i].v += self.curl(pp[i].off) * self.frequency
            ss[i].v = pp[i].v3 + self.curl(pp[i].off)
            ss[i].count +=1 #The sum count of the velocities added to the velocity vector v.
            



if __name__ == "__main__":
    path, fn = os.path.split(__file__)
    bmp = bitmaps.BaseBitmap()
    bmp.InitWith(os.path.join(path, "res", "icons","opycurl.tif"))
    plugins.RegisterObjectPlugin(id=PLUGIN_ID, str="Py-Curl",
                                g=CurlSmoke,
                                description="Opycurl", icon=bmp,
                                info=c4d.OBJECT_PARTICLEMODIFIER)