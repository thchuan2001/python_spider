import pyecharts.options as opts
from pyecharts.charts import Line
import csv
from pyecharts.charts import Pie
from pyecharts.charts import Map
from pyecharts.charts import Boxplot
import scipy.stats as st

# make date_list
date_list=[]
for date in range(5,20):
    if (date<=9):
        t="0"+str(date)
    else:
        t=str(date)
    date_list.append("2021-12-"+t)

cases={}
country_list=[]
for date in date_list:
    with open("./spider_cases/"+date+".csv","r") as f:
        data=f.readlines()[1:]
        for line in data:
            if (len(line)!=0):
                t=line.split(",")
                cases[(t[0],date)]=int(t[1].strip())
            if (t[0] not in country_list):
                country_list.append(t[0])

death={}
for date in date_list:
    with open("./spider_death/"+date+".csv","r") as f:
        data=f.readlines()[1:]
        for line in data:
            if (len(line)!=0):
                t=line.split(",")
                death[(t[0],date)]=int(t[1].strip())

vaccinated={}
for date in date_list:
    with open("./spider_vaccinated/"+date+".csv","r") as f:
        data=f.readlines()[1:]
        for line in data:
            if (len(line)!=0):
                t=line.split(",")
                vaccinated[(t[0],date)]=int(t[1].strip())
new_cases={}
for date in date_list:
    with open("./spider_new/"+date+".csv","r") as f:
        data=f.readlines()[1:]
        for line in data:
            if (len(line)!=0):
                t=line.split(",")
                new_cases[(t[0],date)]=int(t[1].strip())

population={}
with open("./population.csv","r") as f:
    data=f.readlines()[1:]
    for i in data:
        t=i.split(",")
        population[t[0]]=int(float(t[1])*1000)

delete_list=["Eritrea","Vatican","Tonga","Solomon Islands","Samoa","Saint Pierre and Miquelon","Saint Helena","Palau","Cook Islands","Falkland Islands","Kiribati","Macao","Marshall Islands","Micronesia (country)"]

for country in country_list:
    if (population.get(country)==None):
        delete_list.append(country)

delete_list=list(set(delete_list))
for i in delete_list:
    country_list.remove(i)
# 1
total_cases=[]
for date in date_list:
    tot=0
    for country in country_list:
        tot+=cases[(country,date)]
    total_cases.append(tot)

chart = (
    Line()
    .add_xaxis(date_list)
    .add_yaxis("",total_cases)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="全球确诊总数变化图\n(人)"),
        yaxis_opts=opts.AxisOpts(
                type_="value",
                min_=min(total_cases),
                max_=max(total_cases)
            )
        )
    .render("全球确诊变化.html")
)

total_death=[]
for date in date_list:
    tot=0
    for country in country_list:
        tot+=death[(country,date)]
    total_death.append(tot)

chart = (
    Line()
    .add_xaxis(date_list)
    .add_yaxis("",total_death)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="全球死亡病例总数变化图\n(人)"),
        yaxis_opts=opts.AxisOpts(
                type_="value",
                min_=min(total_death),
                max_=max(total_death)
            )
        )
    .render("全球死亡病例数变化.html")
)
# 2
increase_in_15_days=[]
for country in country_list:
    tot=0
    for date in date_list:
        tot+=new_cases[(country,date)]
    increase_in_15_days.append((tot,country))

increase_in_15_days.sort(reverse=True)

increase_top_10_list=[]
for i in range(10):
    increase_top_10_list.append(increase_in_15_days[i][1])

chart = (
    Line()
    .add_xaxis(date_list)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="\n新增数量最多的10个国家新增数量变化图\n（人）"),
        yaxis_opts=opts.AxisOpts(
                type_="value",
                min_=0,
                max_=200000
            )
        )
)
for country in increase_top_10_list:
    increase=[]
    for date in date_list:
        t=new_cases[(country,date)]
        increase.append(t)
    chart.add_yaxis(country,increase,is_symbol_show=False)
chart.render("新增top10.html")

#3
total_cases_dict=[]
for country in country_list:
    tot=cases[(country,date_list[-1])]
    total_cases_dict.append((tot,country))

total_cases_dict.sort(reverse=True)

cases_top_10_list=[]
with open("./累计确诊top10.csv","w",newline="") as f:
    writer=csv.writer(f)
    writer.writerow(["Country","Total Cases"])
    for i in range(10):
        t=total_cases_dict[i][0]
        t/=1000000
        writer.writerow([total_cases_dict[i][1],str(t)+" million"])


# 4
total_cases_dict_rev=[]
others=0
for i in total_cases_dict:
    if (i[0]>1000000):
        total_cases_dict_rev.append((i[1],i[0]/1000000))
    else:
        others+=i[0]/1000000
total_cases_dict_rev.append(("others",others))

chart = (
    Pie()
    .add("", total_cases_dict_rev)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="全球累计确诊饼状图（单位 百万人）"),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical",is_show=False)
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    .render("全球累计确诊饼状图.html")
)

#5
case_ratio=[]
case_ratio_country={}
for country in country_list:
    tot=cases[(country,date_list[-1])]/population[country]*100
    case_ratio.append((tot,country))
    case_ratio_country[country]=tot

case_ratio.sort(reverse=True)

with open("./确诊比例top10.csv","w",newline="") as f:
    writer=csv.writer(f)
    writer.writerow(["Country","Cases Ratio"])
    for i in range(10):
        t=case_ratio[i][0]
        writer.writerow([case_ratio[i][1],str(t)+"%"])

# 6
vacc_ratio=[]
vacc_map=[]
vacc_ratio_country={}
for country in country_list:
    tot=vaccinated[(country,date_list[-1])]/population[country]*100
    vacc_map.append((country,tot))
    vacc_ratio.append((tot,country))
    vacc_ratio_country[country]=tot

chart = (
    Map()
    .add("", vacc_map, "world")
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="全球疫苗接种率地图"),
        visualmap_opts=opts.VisualMapOpts(max_=100),
    )
    .render("全球疫苗接种率地图.html")
)

# 7
vacc_ratio.sort()

with open("./接种率last10.csv","w",newline="") as f:
    writer=csv.writer(f)
    writer.writerow(["Country","Vaccinated Ratio"])
    cnt=0
    i=0
    while (cnt<10):
        i+=1
        t=vacc_ratio[i][0]
        if (t<1e-5):
            continue
        cnt+=1
        writer.writerow([vacc_ratio[i][1],str(t)+"%"])


# 9
death_ratio=[]
death_ratio_country={}
for country in country_list:
    tot=death[(country,date_list[-1])]/population[country]*100
    death_ratio.append((tot,country))
    death_ratio_country[country]=tot

death_ratio.sort(reverse=True)

with open("./死亡比例top10.csv","w",newline="") as f:
    writer=csv.writer(f)
    writer.writerow(["Country","Death Ratio"])
    for i in range(10):
        t=case_ratio[i][0]
        writer.writerow([death_ratio[i][1],str(t)+"%"])

# 最好的10个国家
score=[]
score_map=[]
for country in country_list:
    s=50+vacc_ratio_country[country]-5*case_ratio_country[country]-5*death_ratio_country[country]
    score.append((s,country))
    score_map.append((country,275-s))
score.sort(reverse=True)

with open("./抗疫最好的top10.csv","w",newline="") as f:
    writer=csv.writer(f)
    writer.writerow(["Country","Score"])
    for i in range(10):
        t=score[i][0]
        writer.writerow([score[i][1],str(t)])

#预测
x=range(10)
y=total_cases[:10]
k, b, r_value, p_value, std_err = st.linregress(x, y)
pred=[]
for i in range(15):
    pred.append(k*i+b)

chart = (
    Line()
    .add_xaxis(date_list)
    .add_yaxis("实际",total_cases,is_symbol_show=False)
    .add_yaxis("回归预测值",pred,is_symbol_show=False)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="预测_全球确诊总数变化图"),
        yaxis_opts=opts.AxisOpts(
                type_="value",
                min_=min(total_cases),
                max_=max(total_cases)
            )
        )
    .render("预测_全球确诊变化.html")
)

# 抗疫水平
maxx=-100000
minn=100000
for i in score_map:
    maxx=max(maxx,i[1])
    minn=min(minn,i[1])
chart = (
    Map()
    .add("", score_map, "world")
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="全球抗疫地图"),
        visualmap_opts=opts.VisualMapOpts(max_=190,min_=minn),
    )
    .render("全球抗疫地图.html")
)