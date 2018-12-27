import re
import numpy as np
import io
import json
import plotly
import plotly.graph_objs as go



try:
    open_file = open('C:\\Egor\\PycharmProjects\\dataset\\data\\sub-est2016.csv','r+',encoding='ISO-8859-1')
    keys = tuple(open_file.readline().strip().split(','))
    keys = [key.title() for key in keys]

    df = open_file.read().splitlines()


except EOFError as fille_open_error:
    print("Check filepath or file: ", fille_open_error)

finally:
    open_file.close()

def get_state(s,i):

    st = re.split(r',', s, maxsplit=i+1)
    st = st[i]
    return st

def city_name(s,i):

    st = re.split(r',', s, maxsplit=i+1)
    st = st[i]
    return st

def get_id(s):
    id  = re.findall("\d{15,30}",s)[0]
    return id

def get_POPESTIMATES(s,indexs):
    row_s = re.split(r",",s)
    POPESTIMATES = [row_s[p] for p in indexs]
    return POPESTIMATES






def read_data():
    data_set = {}

    for i in range(len(df)):
        row = df[i].rstrip()
        if not row:
            print("emplty row: ", i)
            continue
        state = get_state(row, list(keys).index('Stname'))
        city = city_name(row, list(keys).index('Name'))
        id = get_id(row)
        POPESTIMATES_index = [keys.index(i) for i in keys if "Popestimate" in i]
        POPESTIMATES = get_POPESTIMATES(row,POPESTIMATES_index)

        if state not in data_set.keys():
            data_set[state]={}

        if city not in data_set[state].keys():
            data_set[state][city]=[]


        data_set[state][city].append({
            "id":id,
            "POPESTIMATES": POPESTIMATES,


        })
    print("data_set")
    return data_set

def dataset_to_json(data_):
    with io.open('data.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_, ensure_ascii=False))


def graph_show(scatter_,bar_,pie_):



    figure = {"data": [
        {
            "x": np.array(list(scatter_.keys())),
            "y": np.array(list(scatter_.values())),
            "type": "scatter",
            "name": "P1",
        },
        {
            "x": np.array(list(bar_.keys())),
            "y": np.array(list(bar_.values())),
            "type": "bar",
            "name": "P1",
            "xaxis": "x2",
            "yaxis": "y2"
        },
        {
            "labels": np.array(list(pie_[0])),
            "values": np.array(list(pie_[1])),
            "type": "pie",
            "name": "P2",
            "textinfo": "none",
            'domain': {'x': [0, 0.45], 'y': [0.55, 1]},
        }
    ], "layout": go.Layout(
        xaxis=dict(domain=[0, 0.45]), yaxis=dict(domain=[0, 0.45]),
        xaxis2=dict(domain=[0.55, 1]), yaxis2=dict(domain=[0, 0.45], anchor='x2'))}
    plotly.offline.plot(figure, filename="plot.html")


if __name__ == '__main__':


    data_s_ = read_data()

    city_of_state = {k:len(list(v)) for k,v in data_s_.items()}

    Abbeville_city_handle = data_s_['Louisiana']['Abbeville city'][0]['POPESTIMATES']
    Abbeville_city_handle_k = [i for i in keys if "Popestimate" in i]

    total_of_state = {}

    # for k,v in data_s_['Louisiana'].items():
    #     for i  in v:
    #         total_of_state[k] = sum([float(ii) for ii in i['POPESTIMATES']])

    total_of_state= {k:sum(list(map(
        lambda i:sum([float(ii) for ii in i['POPESTIMATES']]),v)
    )) for k,v in data_s_['Louisiana'].items()}

    pie_ =(Abbeville_city_handle_k,Abbeville_city_handle)


    graph_show(city_of_state,total_of_state,pie_)


