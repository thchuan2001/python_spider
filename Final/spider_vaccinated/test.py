import requests
t=requests.get("https://ourworldindata.org/explorers/coronavirus-data-explorer?tab=table&zoomToSelection=true&time=2021-12-05&facet=none&uniformYAxis=0&pickerSort=asc&pickerMetric=total_cases&Metric=Confirmed+cases&Interval=Cumulative&Relative+to+Population=false&Color+by+test+positivity=false")
with open("responce.html","w",encoding="utf-8") as f:
    f.write(t.text)