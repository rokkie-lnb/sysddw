import streamlit as st
import re
import requests
from collections import Counter
from bs4 import BeautifulSoup
import jieba
from pyecharts import options as opts
from pyecharts.charts import WordCloud, Bar, Pie, Line, Scatter, Funnel, Polar, Radar


def remove_html_tags(text):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', text)


def get_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = remove_html_tags(soup.get_text())
    return text


def process_text(text, num_words):
    words = jieba.lcut(text)
    word_counter = Counter(words)
    top_words = word_counter.most_common(num_words)
    return word_counter, top_words


def plot_word_cloud(word_counter):
    words = list(word_counter.keys())
    frequencies = list(word_counter.values())

    c = WordCloud()
    c.add("", list(zip(words, frequencies)))
    c.set_global_opts(title_opts=opts.TitleOpts(title="Word Cloud"))
    st_pyecharts(c)
    return c  # 确保返回图表对象

def plot_bar(word_counter):
    words, frequencies = zip(*word_counter)

    c = Bar()
    c.add_xaxis(list(words))
    c.add_yaxis("Frequency", list(frequencies))
    c.set_global_opts(title_opts=opts.TitleOpts(title="Word Frequency Bar Plot"))

    return c


def plot_pie(top_words):
    words, frequencies = zip(*top_words)

    c = Pie(init_opts=opts.InitOpts(width="600px", height="400px"))
    c.add("", [list(z) for z in zip(words, frequencies)],
          radius=["40%", "75%"],
          rosetype="radius",
          label_opts=opts.LabelOpts(is_show=False),
          )
    c.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}", rich={"color": ["#334455", "#2a333d", "#87CEFA"],
                                                                            "shadowColor": "#c23531",
                                                                            "shadowBlur": 10}))
    c.set_global_opts(
        title_opts=opts.TitleOpts(title="Word Frequency Pie Chart", pos_left="center",
                                  title_textstyle_opts=opts.TextStyleOpts(color="#000")),
        legend_opts=opts.LegendOpts(is_show=False))

    return c


def plot_line(top_words):
    words, frequencies = zip(*top_words)

    c = Line()
    c.add_xaxis(words)
    c.add_yaxis("Frequency", frequencies)
    c.set_global_opts(title_opts=opts.TitleOpts(title="Word Frequency Line Chart"))

    return c


def plot_scatter(top_words):
    words, frequencies = zip(*top_words)

    c = Scatter()
    c.add_xaxis(words)
    c.add_yaxis("Frequency", frequencies)
    c.set_global_opts(title_opts=opts.TitleOpts(title="Word Frequency Scatter Plot"))

    return c

def plot_funnel(top_words):
    words, frequencies = zip(*top_words)

    c = Funnel()
    c.add("", list(zip(words, frequencies)))
    c.set_global_opts(title_opts=opts.TitleOpts(title="Word Frequency Polar Chart"))

    return c  # 确保返回图表对象


def plot_polar(top_words):
    words, frequencies = zip(*top_words)

    c = Polar()
    c.add("", list(zip(words, frequencies)))
    c.set_global_opts(title_opts=opts.TitleOpts(title="Word Frequency Polar Chart"))

    return c  # 确保返回图表对象

def plot_radar(top_words):
    words, frequencies = zip(*top_words)

    c = Radar()
    c.add_schema(schema=[opts.RadarIndicatorItem(name=w, max_=100) for w in words])
    c.add("", [frequencies])
    c.set_global_opts(title_opts=opts.TitleOpts(title="Word Frequency Radar Chart"))

    return c  # 确保返回图表对象




def main():
    st.title("Text Analysis with Streamlit")

    url = st.text_input("请输入需要分析的网页 URL")
    num_words = st.sidebar.number_input("请输入需要展示的高频词汇数量", min_value=1, value=20)

    chart_types = {
        "词云图": plot_word_cloud,
        "条形图": plot_bar,
        "饼状图": plot_pie,
        "线状图": plot_line,
        "散点图": plot_scatter,
        "漏斗图": plot_funnel,
        "极坐标图": plot_polar,
        "雷达图": plot_radar,
    }
    selected_chart_type = st.sidebar.selectbox("请选择图表类型", list(chart_types.keys()))

    if url:
        text = get_text_from_url(url)
        word_counter, top_words = process_text(text, num_words)
        selected_chart_func = chart_types[selected_chart_type]
        chart = selected_chart_func(top_words)
        st_pyecharts(chart)

# update the plot_word_cloud function with only top words
def plot_word_cloud(top_words):
    words, frequencies = zip(*top_words)

    c = WordCloud()
    c.add("", list(zip(words, frequencies)), word_size_range=[20, 100])
    c.set_global_opts(title_opts=opts.TitleOpts(title="词云"))

    return c


def st_pyecharts(chart):
    chart.render("temp_chart.html")
    with open("temp_chart.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    st.components.v1.html(html_code, height=500)


if __name__ == "__main__":
    main()