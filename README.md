# Cycler for Home Assistant

This is an integration providing cycler sensor.

### Installation

If you're using HACS - feel free to add https://github.com/PetrS98/ha_cycler.git as custom repository.

Once you've installed the custom integration, add the following to your `configuration.yaml` file:

```yaml
binary_sensor:
  - platform: ha_cycler         # Name of Addon folder
    time_from: "12:00:00"       # Start cycler time
    on_time: "02:30:00"         # On time
    off_time: "00:30:00"        # Off time
    scan_interval: 10           # Scan interval. From 1 to 59 seconds
```
