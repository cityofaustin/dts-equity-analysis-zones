# Equity Analysis Yearly Comparison Tool

This [dash](https://dash.plotly.com/) app enables users to see the changes to Austin's Equity Analysis Zones (EAZs) over time.

The Census Bureau releases new 5-year estimates on an annual basis and this tool will enable longitudinal analysis of
the EAZs.

## Running the tool

You can either build the docker image yourself, or pull the image from our atddocker dockerhub account.

If you are building your own image, be sure you are in the `maps/` subdirectory  
```
$ docker pull atddocker/dts-equity-analysis-zones-map
```

--or--

```
$ docker build -t atddocker/dts-equity-analysis-zones-map . --platform linux/amd64
```

Then, run the script inside the docker container.

```
$ docker run -p 8050:8050 -it --rm atddocker/dts-equity-analysis-zones-map /bin/bash
$ python eaz_comparison_tool.py
```

Visit http://0.0.0.0:8050/ in your browser to view the app.

