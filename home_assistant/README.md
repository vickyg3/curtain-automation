## Home Assistant Component

This is a custom component named `monroe_diy` for home assistant which exposes the curtain as a `cover`.

#### Installation

Simply download [monroe_diy.py](monroe_diy.py) and copy it to `<your_home_assistant_config_directory>/custom_components/cover`.

#### Configuration

To use the custom component, add the following section to your
`configuration.yaml` file:
```yaml
# Example configuration.yaml entry
cover:
  platform: monroe_diy
  covers:
    master_bedroom_curtain:
      friendly_name: "Master Bedroom Curtain"
      ip_address: "192.168.1.25"
      full_open_count: 3
      open_direction: "left"
      close_direction: "right"
```

#### Configuration Parameters

- **ip_address** (*Required*): IP Address of the microcontroller which controls the curtains.
- **full_open_count** (*Required*): Integer which specifies the number of shaft rotations needed to fully open/close the curtain (determined by trial and error).
- **friendly_name** (*Optional*): Name of the curtain as it appears on the home assistant UI.
- **open_direction** (*Optional*): left/right. Direction in which the motor should spin to open the curtain. Defaults to `right`.
- **close_direction** (*Optional*): left/right. Direction in which the motor should spin to close the curtain. Defaults to `left`.
