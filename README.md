## This library isn't maintained anymore!


# pygrundig
Python library for Grundig TV remote control

Install
=======
`pip install pygrundig`


How it works
=======
This python library uses the HTTP API (used by the official Grundig Remote App). This api isn't documented and official.
The library is build with the knowledge of the reverse engineered app.

Currently the library is using as default port 8085. It is possible that your tv is using another port.
To check if your tv uses another port, use nmap:

`nmap -sT <tv ip>`

Example
=======
```python
tv = new PyGrundig("192.168.2.20", "8085")
tv.get_channel_list()
```
