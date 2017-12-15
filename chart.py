#!/usr/bin/python3
from bokeh.models.widgets import Panel, Tabs
from bokeh.plotting import figure, output_file, show, save, ColumnDataSource
from bokeh.models import HoverTool, TapTool, OpenURL, DatetimeTickFormatter
from bokeh.palettes import inferno
import psycopg2, sys, requests, time, random, datetime
from itertools import groupby

max = 2560
offset = 7200
data_query = 'select object_id, array_agg(array[cast(extract(epoch from timestamp) as text), price, address, obj_url, pic_url, description_text, description] order by timestamp asc) as dims from object_info where timestamp >= localtimestamp - interval \'7 days\' group by object_id limit ' + str(max) + ';'
# save the rendered document here
document = "/var/www/html/kv_prices/index.html"
tools_to_show = 'box_zoom,pan,save,hover,reset,tap,wheel_zoom'
def plot():
    cursor.execute(data_query)
    data = cursor.fetchall()
    # get all items that have changed prices
    data_filtered = [[object_id, points] for (object_id, points) in data if len(set([point[1] for point in points])) != 1]

    # tab 1
    plot_all = figure(tools = tools_to_show, width = 1600, height = 800, x_axis_type = 'datetime')
    plot_all.multi_line('x', 'y', source=get_plot_data_source(data), color = 'color', line_width = 'thicc')
    get_plot_stuff(plot_all)

    # tab 2
    plot_filtered = figure(tools = tools_to_show, width = 1600, height = 800, x_axis_type = 'datetime')
    plot_filtered.multi_line('x', 'y', source=get_plot_data_source(data_filtered), color = 'color', line_width = 'thicc')
    get_plot_stuff(plot_filtered)

    tab1 = Panel(child=plot_all, title="All apartments")
    tab2 = Panel(child=plot_filtered, title="Changed prices")
    tabs = Tabs(tabs=[ tab1, tab2 ])
  # show(p)
    output_file(document)
    save(tabs)
    print("Saved.")

def get_plot_data_source(data):
    xs = [[int(float(datapoint[0])) * 1000 for datapoint in points] for (object_id, points) in data]
    ys = [[int(datapoint[1]) + random.randint(-100,100) for datapoint in points] for (object_id, points) in data]
    source = ColumnDataSource({
        'x': xs,
        'y': ys,
        'object_id': [object_id for (object_id, points) in data],
        'address': [points[-1][2] for (object_id, points) in data],
        #TODO: cannot set different price for different data points, maybe a bug, maybe using it wrong; includind the entire price history for each point
        'price': [" -> ".join([str(price) + "€" for price in [x[0] for x in groupby([point[1] for point in points])]]) for (object_id, points) in data],
        'link': [points[-1][3] for (object_id, points) in data],
        'pic': [points[-1][4] for (object_id, points) in data],
        'desctext': [points[-1][5] for (object_id, points) in data],
        'desc': [points[-1][6] for (object_id, points) in data],
        'lastdl': [datetime.datetime.fromtimestamp(int(float(points[-1][0])) - offset).strftime('%Y-%m-%d %H:%M:%S') for (object_id, points) in data],
        'color': [inferno(min(256, len(data)))[index % min(256, len(data))] for index in range(len(data))],
        # thicker line if prices have changed
        'thicc': [5 if len(set([point[1] for point in points])) != 1 else 1 for (object_id, points) in data]
    })
    return source

def get_plot_stuff(plot):
    plot.xaxis.formatter=DatetimeTickFormatter(
      seconds=["%d %B %Y"],
      minutes=["%d %B %Y"],
      hours=["%d %b %Y"],
      days=["%d %b %Y"],
      months=["%d %b %Y"],
      years=["%d %b %Y"])
    hover = plot.select(dict(type=HoverTool))
    hover.tooltips = [("pic", "<img src='@pic' alt='' />"), ("id", "@object_id"), ("Address", "@address"), ("Info", "@desctext"), ("Description", "@desc"), ("Price", "@price"), ("Last scraped", "@lastdl")]
    hover.mode = 'mouse'
    taptool = plot.select(type=TapTool)
    taptool.callback = OpenURL(url="@link")

def connect():
    conn_string = "host='localhost' dbname='kv_prices' user='USER HERE' password='PASS HERE'"
    print("Connecting to database...")
    global conn
    global cursor
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print("Connected!\n")

while True:
    connect()
    plot()
    conn.close()
    print("Sleeping...")
    time.sleep(600)



