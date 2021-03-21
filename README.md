# Minimal proSmart - MQTT Gateway

Minimal MQTT interface for proSmart Thermostat devices.

Reading Temperature, Humidity and LDR (Light Dependent Resistor) sensor values
and setting the target temperature functions are supported.

Designed for controlling proSmart Thermostat using MQTT capable
tools (like Home Assistant).

Test device used: [Computherm B300](https://computherm.info/hu/wi-fi_termosztatok/computherm_b300).

## Auth Token and UserID

UserID is stored in the Browser Local Storage under logged_user key
(JSON key "ID").

Auth Token is the pss.auth cookie stored as a cookie in the logged in
Browser.

## MQTT Topics

| Value | Topic | Dimension |
| ----- | ----- | --------- |
| Temperature | prosmart/[device_name]/temperature | ℃ |
| Humidity    | prosmart/[device_name]/humidity    | % |
| LDR         | prosmart/[device_name]/ldr         | % |
| Temperature to Set | prosmart/[device_name]/setpoint | ℃/100 | 
| Temperature to Set (modify) | prosmart/[device_name]/set_temp | ℃ |

