# tuya-cloud-bulb-user-interface

This is a continuation to my previous project, along with new user interface with django framework, previous project: https://github.com/Anurag-Varma/tuya-cloud-smart-bulb

<br>
<h3>Installing:</h3>

```
pip install django
```
```
pip install tuya-bulb-control --upgrade
```
```
pip install colormap
```
<br>

[![Watch the video]()](https://user-images.githubusercontent.com/66156396/124347513-c8181980-dc02-11eb-9398-861cfad77c10.mp4)



<br>
<h3>Demo Code:</h3>

```Python
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from tuya_bulb_control import Bulb
from colormap import hex2rgb
import random

CLIENT_ID = ''    # Access ID or Client ID
SECRET_KEY = ''   # Access Secret or Client Secret
DEVICE_ID = ''    # Devise id which is online to control
REGION_KEY = ''   # Region key eg: in for india, eu for europe, us for usa, cn for china, etc based on region where the device is there 

flag=0
globalcolour=(255,255,255)

bulb = Bulb(
    client_id=CLIENT_ID,
    secret_key=SECRET_KEY,
    device_id=DEVICE_ID,
    region_key=REGION_KEY
)

def index(request):
    template = loader.get_template('bulb/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def action(request):
    global flag
    global globalcolour
    e=0
    try:
        bulbval=request.GET['bulb']
        val=request.GET['val']
        color=request.GET['color']

        if bulbval=="on":
            bulb.turn_on()
        elif bulbval=="off":
            flag=0
            bulb.turn_off()
        elif bulbval=="bright":
            x=int(val)
            bulb.set_bright_v2(value=x)
            bulb.set_colour_v2(rgb=globalcolour)
        elif bulbval=="color":
            flag=0
            globalcolour=hex2rgb(color)
            bulb.set_colour_v2(rgb=hex2rgb(color))
        elif bulbval=="toggle":
            flag=0
            bulb.set_toggle()
        if bulbval=="disco":
            if flag==0:
                flag=1
            else:
                flag=0
                bulb.set_colour_v2(rgb=hex2rgb(color))
            while flag==1:
                r=random.randint(0, 255)
                g=random.randint(0, 255)
                b=random.randint(0, 255)
                bulb.set_colour_v2(rgb=(r,g,b))
                print(r,g,b)
    except Exception as e:
        flag=0
        print(str(e))

    return redirect(index)
```
<br>

<h3>Steps:</h3>

#### Step 1: CLIENT_ID and SECRET_KEY
- Register or Login on <a href="https://auth.tuya.com" target="_blanck">Tuya</a>.
1. Create a cloud development project <a href="https://iot.tuya.com/cloud" target="_blanck">Cloud -> Project</a>.
2. After successful creation, you will receive the **Client ID** and **Secret Key**.


#### Step 2: DEVICE_ID
1. Install **Tuya Smart** app or **Smart Life** app on your mobile phone.
2. Go to <a href="https://iot.tuya.com/cloud/appinfo/cappId/device" target="_blanck">Cloud -> Link Devices</a> page.
3. Selecting a tab **Link Devices by App Account**.
4. Click **Add App Account** and scan the QR code with **Tuya Smart** app or **Smart Life** app.
5. Now you can go to devices <a href="https://iot.tuya.com/cloud/appinfo/cappId/deviceList" target="_blanck">Cloud -> Device List</a> and copy **Device ID**.
    * Notes: Try to select a your region if devices are not displayed.


#### Step 3: Request access to API calls
Go to <a href="https://iot.tuya.com/cloud/appinfo/cappId/setting" target="_blanck">Cloud -> API Group</a> and enable **Authorization management**, **Device Management** and **Device Control**.

**Done!**
