# Botpartner CoT - Device GPIO Controller for Pi2

## Requires

 * python version: 2.7
 * Hardware platfrom : raspberry pi 2 B+

## Usage

 * Set up the COT SMQ server's ip, connect port number and device UUID
```python

#Json format for __YOUR_COT_SMQ_DOMAINNAME__:__YOUR_COT_SMQ_PORT__
server ='__YOUR_COT_SMQ_SERVER_IP__'
port = __YOUR_COT_SMQ_PORT__
SocketTimeout=1
vendor = '__YOUR_VENDER_ID__'
device = '__YOUR_DEVICE_ID__'
token  = '__YOUR_COT_SMQ_TOKEN__'

send_string={
    'vendor': vendor,
    'device': device,
    'uuid'  : '__YOUR_DEVICE_UUID__',
    'token' :  token,
    'action': 'update'
    }

```

   Notice : there are file type to produce log file
   Debug mode :
   "logging.basicConfig(level=logging.INFO,filename=Test_LOG_PATH,format=LOG_FORMAT)"
   Operation Mode :
   "logging.basicConfig(level=logging.INFO,filename=LOG_PATH,format=LOG_FORMAT)"
   (Default is Operation mode. The debug mode will produce very large log file.)
 * Complier python py file to pyc file
   "python -m socket_gpio.py"
 * change the owner and execution mode to pyc file
   "sudo chown root:root socket_gpio.pyc"
   "sudo chmod a+x socket_gpio.pyc"
 * move pyc file to exection path folder
   "sudo mv socket_gpio.pyc /usr/local/sbin/"
 * set up the lunch script to /etc/init.d
   "sudo mv socket_gpio /etc/init.d/"
 * Set the /usr/local/sbin/socket_gpio.pyc as the boot on daemon

## License

(The MIT License)

Copyright (c) 2016 Shawn Lin (edwin2619@gmail.com) , BotPartner Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
