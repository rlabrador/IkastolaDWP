import json 
import sys 
if ':' not in config.version_id:  
  # The default server version_id does not contain ':'  
  sys.path.append("lib")  
  import ptvsd  #ptvsd.settrace() equivalent  
  ptvsd.enable_attach(secret = 'joshua')  
  ptvsd.wait_for_attach()

