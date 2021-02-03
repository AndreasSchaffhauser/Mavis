from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from os import listdir
from os.path import isfile, join
import os.path
import time
import csv

# JavaScript: HTML5 File drop
# source            : https://gist.github.com/florentbr/0eff8b785e85e93ecc3ce500169bd676
# param1 WebElement : Drop area element
# param2 Double     : Optional - Drop offset x relative to the top/left corner of the drop area. Center if 0.
# param3 Double     : Optional - Drop offset y relative to the top/left corner of the drop area. Center if 0.
# return WebElement : File input
JS_DROP_FILES = "var c=arguments,b=c[0],k=c[1];c=c[2];for(var d=b.ownerDocument||document,l=0;;){var e=b.getBoundingClientRect(),g=e.left+(k||e.width/2),h=e.top+(c||e.height/2),f=d.elementFromPoint(g,h);if(f&&b.contains(f))break;if(1<++l)throw b=Error('Element not interactable'),b.code=15,b;b.scrollIntoView({behavior:'instant',block:'center',inline:'center'})}var a=d.createElement('INPUT');a.setAttribute('type','file');a.setAttribute('multiple','');a.setAttribute('style','position:fixed;z-index:2147483647;left:0;top:0;');a.onchange=function(b){a.parentElement.removeChild(a);b.stopPropagation();var c={constructor:DataTransfer,effectAllowed:'all',dropEffect:'none',types:['Files'],files:a.files,setData:function(){},getData:function(){},clearData:function(){},setDragImage:function(){}};window.DataTransferItemList&&(c.items=Object.setPrototypeOf(Array.prototype.map.call(a.files,function(a){return{constructor:DataTransferItem,kind:'file',type:a.type,getAsFile:function(){return a},getAsString:function(b){var c=new FileReader;c.onload=function(a){b(a.target.result)};c.readAsText(a)}}}),{constructor:DataTransferItemList,add:function(){},clear:function(){},remove:function(){}}));['dragenter','dragover','drop'].forEach(function(a){var b=d.createEvent('DragEvent');b.initMouseEvent(a,!0,!0,d.defaultView,0,0,0,g,h,!1,!1,!1,!1,0,null);Object.setPrototypeOf(b,null);b.dataTransfer=c;Object.setPrototypeOf(b,DragEvent.prototype);f.dispatchEvent(b)})};d.documentElement.appendChild(a);a.getBoundingClientRect();return a;"

def drop_files(element, files, offsetX=0, offsetY=0):
    driver=element.parent
    isLocal=not driver._is_remote or '127.0.0.1' in driver.command_executor._url
    paths=[]
    
    # ensure files are present, and upload to the remote server if session is remote
    for file in (files if isinstance(files, list) else [files]) :
        if not os.path.isfile(file) :
            raise FileNotFoundError(file)
        paths.append(file if isLocal else element._upload(file))
    
    value='\n'.join(paths)
    elm_input=driver.execute_script(JS_DROP_FILES, element, offsetX, offsetY)
    elm_input._execute('sendKeysToElement', {'value': [value], 'text': value})


# mypath="C:\\Users\\aschaffhauser\\Desktop\\StegExpose\\images\\mode-2\\deobfuscated\\256x256"
mypath="C:\\Users\\aschaffhauser\\Desktop\\StegExpose\\images\\mode-2\\obfuscated\\256x256"
# mypath="C:\\Users\\aschaffhauser\\Desktop\\StegExpose\\images\\mode-2\\clean\\256x256\\png"

# mypath="C:\\Users\\aschaffhauser\\Desktop\\StegExpose\\images\\mode-1\\deobfuscated\\deob_1"
# mypath="C:\\Users\\aschaffhauser\\Desktop\\StegExpose\\images\\mode-1\\deobfuscated\\deob_2"
# mypath="C:\\Users\\aschaffhauser\\Desktop\\StegExpose\\images\\mode-1\\obfuscated\\ob_1"
# mypath="C:\\Users\\aschaffhauser\\Desktop\\StegExpose\\images\\mode-1\\obfuscated\\ob_2"

onlyfiles=[f for f in listdir(mypath) if isfile(join(mypath, f))]

filename = "256x256_mode_2_ob_mcafee"

with open(filename + '.csv', mode='a', newline='', encoding='utf-8') as result_file:
    result_writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    result_writer.writerow(['Filename',\
    'Suspicious',\
    'Confidence Level',\
    'Score',\
    'Scan Time (ms)',\
    'Errors'])

WebElement.drop_files=drop_files
driver=webdriver.Chrome()
driver.get("https://www.mcafee.com/enterprise/en-us/downloads/free-tools.html")
time.sleep(15)
link = driver.find_element_by_link_text('Steganography Analysis Tool')
link.click()

default_time=5

for x in range(len(onlyfiles)):

    try:
        dropzone=driver.find_element_by_id("sdidropzone")
        dropzone.drop_files(mypath + "\\" + onlyfiles[x])
        time.sleep(default_time)
        results=driver.find_element_by_id("sdi-results")
        results=results.text.split("\n")
        suspicious=results[0].split()[1]
        confidence_level=results[1].split()[2]
        score=results[2].split()[1]
        scan_time=results[3].split()[2]
        errors=results[4].split()[1]
        
        print(x)
        print(suspicious)
        print(confidence_level)
        print(score)
        print(scan_time)
        print(errors)
        print(default_time)
        print()

        with open(filename + '.csv', mode='a', newline='', encoding='utf-8') as result_file:
            result_writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            result_writer.writerow([onlyfiles[x],\
            str(suspicious),\
            str(confidence_level),\
            str(score).replace(".", ","),\
            str(scan_time),\
            str(errors)])

    except IndexError as ie:
        with open(filename + '.csv', mode='a', newline='', encoding='utf-8') as result_file:
            result_writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            result_writer.writerow([onlyfiles[x],\
            'not_tested',\
            'not_tested',\
            'not_tested',\
            'not_tested',\
            'not_tested'])

    # if x==10:
    #    break

driver.quit()

