import numpy as np

class MapElement:
    def __init__(self,vec:np.ndarray,dist:float,val):
        self.vec = vec
        self.val = val
        self.dist = dist

class CosEmbeddedMap:
    def __init__(self,vec_size:int = 160):
                
        self.ref_vector = np.ones(vec_size,dtype=np.float32)*0.07905694150420949
                
        self.data:list[MapElement] = []
        
        self._max_val = 0
        self._min_val = 0
        
    def push(self,vec:np.ndarray,val):
        
        dist_cos = np.dot(vec,self.ref_vector)
        
        if len(self.data) == 0:
            self._max_val = dist_cos
            self._min_val = dist_cos
            self.data.append(MapElement(vec,dist_cos,val))
            return False
        
        if dist_cos < self._min_val or dist_cos > self._max_val:
            self.data.append(MapElement(vec,dist_cos,val))
            
            self._max_val = max(self._max_val,dist_cos)
            self._min_val = min(self._min_val,dist_cos)
            return False
                
        elem = self.search(vec)
        
        if elem is not None:
            print("Val: ",elem.val)
            elem.val = val 
            return True
            
        self.data.append(MapElement(vec,dist_cos,val))
        
        self._max_val = max(self._max_val,dist_cos)
        self._min_val = min(self._min_val,dist_cos)
        return False    
            
    def search(self,vec:np.ndarray)->MapElement|None:  
        
        if len(self.data) == 0:
            return None 
        
        dist_cos = np.dot(vec,self.ref_vector)
        
        if dist_cos < self._min_val or dist_cos > self._max_val:
            return None
        
        self.data = sorted(self.data,key = lambda x: x.dist)
        
        p = 0
        q = len(self.data)
        
        while q - p > 10:
            
            mindpoint = int((p+q)/2)
            
            elem = self.data[mindpoint]
            
            if abs(elem.dist - dist_cos) < 0.1:
                return elem
            
            if dist_cos > elem.dist:
                p = mindpoint
            else:
                q = mindpoint
                
        
        for elem in self.data[p:q]:
            if abs(elem.dist - dist_cos) < 0.1:
                return elem
            
        return None
    
    def remove(self,elem):
        
        if len(self.data) == 0:
            return False
        
        try:
            self.data.remove(elem)
        except ValueError:
            return False
        
        self.data = sorted(self.data,key = lambda x:x.dist)
        
        self._min_val = self.data[0].dist
        self._max_val = self.data[-1].dist
        
        return True