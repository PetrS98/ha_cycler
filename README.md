# OTE Energy Cost Sensor for Home Assistant

This is an integration providing price of energy from ote-cr.cz, attributes as solo sensors, lowest price sensor and highest price sensor.
And binary status sensors for lowest and highest price active.

### Installation

If you're using HACS - feel free to add https://github.com/PetrS98/ote_energy_parser_czk as custom repository.

Once you've installed the custom integration, add the following to your `configuration.yaml` file:

```yaml
sensor:
  - platform: ha_cycler         # Name of Addon folder
    time_from: "13:15:00"       # Start cycler time
    on_time: "00:01:00"         # On time
    off_time: "00:01:00"        # Off time
    scan_interval: 10           # Scan interval. From 1 to 59 seconds
```
