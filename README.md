# QDU: Quick Daily Updates

A simple terminal application (tested on Linux) meant to give a
brief overview of the current news.

## How to use it

Currently one can run the application using

```
python qdu.py --source provider-name
```

The sources are to be configured in `providers.json`.

If one wants to display two different news sources at the 
same time use a comma, like

```
python qdu.py --source provider-1-name,provider-2-name
```

In the case that no sources are specified

```
python qdu.py
```

a default provider will be chosen, based on the 
default provider set in `settings.json`.


## What to do

* Fix time displays
* (Maybe) display local news based on geolocation
* Etc