# Equity Analysis Yearly Comparison Tool

Hosted at: [equitytool.austinmobility.io](https://equitytool.austinmobility.io/).

![eaz tool example image](../docs/imgs/eaz_tool.png)

This [dash](https://dash.plotly.com/) app enables users to see the changes to Austin's Equity Analysis Zones (EAZs) over time.

The Census Bureau releases new 5-year estimates on an annual basis and this tool will enable longitudinal analysis of
the EAZs.

## Running the tool

You can either build the docker image yourself, or pull the image from our atddocker dockerhub account.

If you are building your own image, be sure you are in the `maps/` subdirectory

```
docker pull atddocker/dts-equity-analysis-zones-map
```

--or--

```
docker build -t atddocker/dts-equity-analysis-zones-map . --platform linux/amd64
```

Then, run the script inside the docker container.

```
docker run -p 8050:8050 -it --rm atddocker/dts-equity-analysis-zones-map /bin/bash
python eaz_comparison_tool.py
```

Visit http://0.0.0.0:8050/ in your browser to view the app.

Alternatively, you can use docker compose. There is a placeholder `README.md` file in `haproxy/ssl/` that needs to be deleted in order for haproxy to run without errors. Then run

```
docker compose up

```

and visit https://localhost:9000/

## Deployment

[Link to internal docs](https://app.gitbook.com/o/-LzDQOVGhTudbKRDGpUA/s/-M4Ul-hSBiM-3KkOynqS/equity-analysis-zone-tool)

### SSL/TLS Certificate

The SSL/TLS certificate is sourced via [Let's Encrypt](https://letsencrypt.org/) and is manually renewed every 60 days.
