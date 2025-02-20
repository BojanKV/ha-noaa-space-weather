## Install
1. Copy files from `www` to `config/www`
2. `Dashboard` > `Edit` > 3 button menu > `Manage resources`
3. Enter these 3 resources:
   ```
   /local/space-weather-24hr-max-card.js?v=1
   /local/space-weather-card.js?v=1
   /local/space-weather-pred-card.js?v=1
   ```
## Use
To add these custom cards, create a card of the "Manual" type.

```yaml
type: space-weather-current
```
```yaml
type: space-weather-prediction-1day
```
```yaml
type: space-weather-24hr-max
```

## GloTEC Map

1. Enable the [Generic Camera](https://www.home-assistant.io/integrations/generic/) integration.
2. Set the `Still Image URL` to your chosen source (see below).
3. Set the `Frame Rate (Hz)` to `0.0016666666666667` (10 minute refresh rate).
4. Create this card on the dashboard:
    ```yaml
    type: picture-entity
    entity: camera.[your entity name]
    show_state: false
    show_name: false
    camera_view: auto
    ```

**NOAA Generated:** `https://services.swpc.noaa.gov/experimental/images/animations/glotec/100asm_urt/latest.png`

**Locally Generated:** `http://[server IP]:5000/global`
