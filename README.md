# Minimal proSmart - MQTT Gateway

Minimal MQTT interface for proSmart Thermostat devices.

> NOTE: This project is obsolete. If interested in Home Assistant integration, look for the awesome work of [zadoli](https://github.com/zadoli): [ha-computherm-b](`https://github.com/zadoli/ha-computherm-b)

Reading Temperature, Humidity and LDR (Light Dependent Resistor) sensor values
and setting the target temperature functions are supported.

Designed for controlling proSmart Thermostat using MQTT capable
tools (like Home Assistant).

Test device used: [Computherm B300](https://computherm.info/hu/wi-fi_termosztatok/computherm_b300).

## Access Token and UserID

UserID is stored in the Browser Local Storage under logged_user key
(JSON key "ID").

Access Token is the pss.auth cookie stored as a cookie in the logged in
Browser.

## MQTT Topics

| Value | Topic | Dimension |
| ----- | ----- | --------- |
| Temperature | prosmart/[device_name]/temperature | ℃ |
| Humidity    | prosmart/[device_name]/humidity    | % |
| LDR         | prosmart/[device_name]/ldr         | % |
| Temperature to Set | prosmart/[device_name]/setpoint | ℃ | 
| Temperature to Set (modify) | prosmart/[device_name]/set_temp | ℃ |

## Home Assistant Example Configuration

Example entry for `configuration.yml`:

```yaml
climate:
  - platform: mqtt
    current_temperature_topic: "prosmart/MyDevice/temperature"
    max_temp: 45.0
    min_temp: 10.0
    temp_step: 0.1
    name: "MyDevice"
    temperature_command_topic: "prosmart/MyDevice/set_temp"
    temperature_state_topic: "prosmart/MyDevice/setpoint"
```
