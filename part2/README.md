## Part II scripts
All data for this part of the project have been uploaded to Dropbox and can be accessed at https://www.dropbox.com/sh/llwzolpa8kwucnb/AABPfc_eipd8qAos78l36gSta?dl=0

Unless stated differently in this README please look at the general instructions in the root folder README to run the scripts. 

### Weather files
`weather.tsv` was generated by running `Wunderground scraper+parser.ipynb`.

`rain.py`, `snow.py` and `temp.py` were all run with `weather.tsv`. They can all be run with the following command:

```
spark-submit SCRIPT_NAME.py weather.tsv
```

### Noise Complaint and DUI Scripts
`avg_day_noise_complaints.py` is to be run on noise complaint filtered 311 Complaint data (available in the DropBox) can be run with the following command:
```
hfs -put noise_complaints.csv
spark-submit avg_day_noise_complaints.py /user/YOUR_NETID/noise_complaints.csv
```

`daily_noise_complaints.py` is also to be run on noise complaint filtered 311 Complaint data as we did in the previous script and can be run with the following command:
```
spark-submit daily_DUI_crimes.py /user/YOUR_NETID/noise_complaints.csv
```

`daily_DUI_crimes.py` is to be run on our original cleaned csv (assuming that is still in your HDFS directory and can be run with the following command:
```
spark-submit daily_DUI_crimes.py /user/YOUR_NETID/cleaned_data.csv
```

### Pluto Dataset Processing
Requires: [PLUTO](https://www1.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page) dataset files located in ../data/PLUTO

`analyze_pluto.py` goes through the PLUTO datset files and returns a file containing int(year), int(precinct), float(mean property value by square feet) in tsv format.
```
spark-submit analyze_pluto.py
```
