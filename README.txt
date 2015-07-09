GitHub installé sur ma base Windows Visual Studio
suivi tuto :
http://joesdevnotepad.blogspot.co.at/2014/07/remote-debug-google-app-engine.html
#################
 Remote debug Google App Engine development server with Python Tools for Visual Studio 2013
I mainly post this, so I will remember the next time I try it. Also because I couldn't find a complete solution anywhere else.

What I tried to do: 
After installing the Google Cloud SDK and running dev_appserver.py I wanted to debug my simple test application so I could then start to write more complicated code. For coding i use Visual Studio 2013 Pro and Python Tools for Visual Studio

I quickly ran into some trouble because to debug GAE with ptvs is not supported by ptvs.

But with a little help of some google-fu and a whole afternoon I got it running, like this:


Create A File to Inject remote debugger
1a. Get ptvsd from Microsoft Visual Studio Python Tools, if you dont have it already.
1. make a new python file "pydevd_startup.py"
import json 
import sys 
if ':' not in config.version_id:  
  # The default server version_id does not contain ':'  
  sys.path.append("lib")  
  import ptvsd  #ptvsd.settrace() equivalent  
  ptvsd.enable_attach(secret = 'joshua')  
  ptvsd.wait_for_attach()

3. Save it in your working directory of your app
4. for more info look at the pytool remote debuging docu I mentioned above


Edit Project Settings in VS 2013
Now open your Project Settings in VS and choose either a) or b)
A. Works with gcloud preview app (newer, autorestarts after changes)

    ?
    1
    2
    3
    	
    <b>Launch Mode->Standard Python Launcher</b>
    <b>General->Startup File: </b>  
    C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin\..\./lib\googlecloudsdk\gcloud\gcloud.py

    ?
    1
    	
    <b>General->Working Directory:</b>  

    ?
    1
    	
    .

    ?
    1
    	
    <b>Debug->Search Paths:</b>

    ?
    1
    	
    C:\{path-to}\Cloud SDK\google-cloud-sdk\lib

    ?
    1
    2
    3
    	
    <b>Debug->Script Arguments: </b>
       
    preview app run . --python-startup-script "{path-to}\pydevd_startup.py" --max-module-instances="default:1"

B. Works with dev_appserver.py (older, but more reliable?)

    ?
    1
    2
    3
    4
    5
    	
    Launch Mode->Standard Python Launcher
    General->Startup File: C:\{path-to}\Cloud SDK\google-cloud-sdk\bin\dev_appserver.py
    General->Working Directory: .
    Debug->Search Paths: C:\{path-to}\Cloud SDK\google-cloud-sdk\lib
    Debug->Script Arguments:  --python_startup_script="{path-to-your, e.g. "."}\pydevd_startup.py" --automatic_restart=no --max_module_instances="default:1" "{path-to-your, e.g. "."}\app.yaml"

You could probaly also use . instead of <path-to-your-app> but I wanted to be safe.


Run Debugger
With <Ctrl+F5> you run the debugger, without debuging. This sound weird, but we are actually not debugging right now, just running the dev server which than starts our script to inject the debugger code and wait for our remote debugger to connect, which will happen in the next step


Start Remote Debugger
DEBUG->Attach to Process <Crtl+Alt+P>
Qualifier: tcp://joshua@localhost:5678 <ENTER>

joshuha is your secret key. If you want to change it (and you should), you also have to change it in the pydevd_startup.py. See pytool reference for more info.

But apart of this security concerns your next step should be:

Be really happy!
You now can remote debug your application locally (erm, weird). To test this you probably should use a breakpoint in your own script. I choose the

    return "hello world!" 

line for this.

If you have any question, please ask. In the end it seems really simple, but to get this going was rough. Especially because pytools said, they don't support it. Microsoft probably doesn't want people to use GAE with their own Azure Cloud in the running


Start Debugging for real!
Open http://localhost:8080 in a browser (or any other address you configure your app to use). Now it should invoke the breaking point. If you are done and reload the site, it starts all over again. If you really want to end debugging or change some code, you have to restart the server and attach again. don't forget to close the terminal window with the server open (use <Crtl+C> )
#################
