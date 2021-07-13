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