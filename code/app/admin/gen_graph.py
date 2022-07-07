from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Liquid, Page, Pie, Tab, Geo
from pyecharts.commons.utils import JsCode
from pyecharts.components import Table
from pyecharts.faker import Faker
import random

from ..models import db, User, News


def bar_datazoom_slider() -> Bar:
    c = (
        Bar()
            .add_xaxis(Faker.days_attrs)
            .add_yaxis("商家A", Faker.days_values)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Bar-DataZoom（slider-水平）"),
            datazoom_opts=[opts.DataZoomOpts()],
        )
    )
    return c


def line_markpoint() -> Line:
    c = (
        Line()
            .add_xaxis(Faker.choose())
            .add_yaxis(
            "商家A",
            Faker.values(),
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min")]),
        )
            .add_yaxis(
            "商家B",
            Faker.values(),
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Line-MarkPoint"))
    )
    return c


def pie_rosetype() -> Pie:
    v = Faker.choose()
    c = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(v, Faker.values())],
            radius=["30%", "75%"],
            center=["25%", "50%"],
            rosetype="radius",
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add(
            "",
            [list(z) for z in zip(v, Faker.values())],
            radius=["30%", "75%"],
            center=["75%", "50%"],
            rosetype="area",
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Pie-玫瑰图示例"))
    )
    return c


def grid_mutil_yaxis() -> Grid:
    x_data = ["{}月".format(i) for i in range(1, 13)]
    bar = (
        Bar()
            .add_xaxis(x_data)
            .add_yaxis(
            "蒸发量",
            [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3],
            yaxis_index=0,
            color="#d14a61",
        )
            .add_yaxis(
            "降水量",
            [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3],
            yaxis_index=1,
            color="#5793f3",
        )
            .extend_axis(
            yaxis=opts.AxisOpts(
                name="蒸发量",
                type_="value",
                min_=0,
                max_=250,
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#d14a61")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
            )
        )
            .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value",
                name="温度",
                min_=0,
                max_=25,
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#675bba")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                name="降水量",
                min_=0,
                max_=250,
                position="right",
                offset=80,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#5793f3")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
            ),
            title_opts=opts.TitleOpts(title="Grid-多 Y 轴示例"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        )
    )

    line = (
        Line()
            .add_xaxis(x_data)
            .add_yaxis(
            "平均温度",
            [2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2],
            yaxis_index=2,
            color="#675bba",
            label_opts=opts.LabelOpts(is_show=False),
        )
    )

    bar.overlap(line)
    return Grid().add(
        bar, opts.GridOpts(pos_left="5%", pos_right="20%"), is_control_axis_index=True
    )


def liquid_data_precision() -> Liquid:
    c = (
        Liquid()
            .add(
            "lq",
            [0.3254],
            label_opts=opts.LabelOpts(
                font_size=50,
                formatter=JsCode(
                    """function (param) {
                        return (Math.floor(param.value * 10000) / 100) + '%';
                    }"""
                ),
                position="inside",
            ),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Liquid-数据精度"))
    )
    return c


def table_base() -> Table:
    table = Table()

    headers = ["City name", "Area", "Population", "Annual Rainfall"]
    rows = [
        ["Brisbane", 5905, 1857594, 1146.4],
        ["Adelaide", 1295, 1158259, 600.5],
        ["Darwin", 112, 120900, 1714.7],
        ["Hobart", 1357, 205556, 619.5],
        ["Sydney", 2058, 4336374, 1214.8],
        ["Melbourne", 1566, 3806092, 646.9],
        ["Perth", 5386, 1554769, 869.4],
    ]
    table.add(headers, rows).set_global_opts(
        title_opts=opts.ComponentTitleOpts(title="Table")
    )
    return table


def gender_pie() -> Pie:

    male = len(User.query.filter_by(gender=1).all())
    female = len(User.query.filter_by(gender=2).all())
    c = (
        Pie()
            .add(
            "",
            [['male', male], ['female', female]]
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="男女比例"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c


def age_bar() -> Bar:
    # 调数据库
    age = [i for i in range(100)]
    num = [i for i in range(50)]
    c = (
        Bar()
            .add_xaxis(age)
            .add_yaxis("年龄分布", num)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="年龄分布"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
    )
    return c


def city_bar() -> Bar:
    # 调数据库
    db.session.execute("select count(*) from user group by user.city having user.city != '' ")
    city = ['北京', '上海', '吉安']
    num = [i for i in range(3)]
    c = (
        Geo()
            .add_schema(maptype="china")
            .add("城市分布", [list(z) for z in zip(city, num)])
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(is_piecewise=True),
            title_opts=opts.TitleOpts(title="城市分布"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c


def news_click_rate() -> Bar:
    # 调数据库
    news_class_name = ['class' + str(i) for i in range(20)]
    click_rate = [i / 100 for i in range(20)]
    love_num = [i / 100 for i in range(20)]
    c = (
        Bar()
            .add_xaxis(news_class_name)
            .add_yaxis("新闻点击率", click_rate)
            .add_yaxis("新闻喜好分布", love_num)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="新闻喜好分布和点击率"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
    )
    return c


def news_collection() -> Bar:
    # 调数据库
    news_class_name = ['class' + str(i) for i in range(20)]
    collection_num = [i for i in range(20)]
    c = (
        Bar()
            .add_xaxis(news_class_name)
            .add_yaxis("新闻收藏数", collection_num)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="新闻收藏数"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
    )
    return c


def user_numAndIncrease() -> Grid:
    # 调数据库
    user_num = [random.randint(i, i * 10) for i in range(365)]
    user_online = [random.randint(0, 100) for i in range(365)]
    user_increase = [user_num[i] - user_num[i - 1] for i, _ in enumerate(user_num)]
    x_data = ["{}月{}日".format(i, j) for i in range(1, 13) for j in range(1, 31)]
    bar = (
        Bar()
            .add_xaxis(x_data)
            .add_yaxis(
            "用户存量",
            user_num,
            yaxis_index=0,
            color="#d14a61",
        )
            .add_yaxis(
            "用户上线量",
            user_online,
            yaxis_index=1,
            color="#5793f3",
        )
            .extend_axis(
            yaxis=opts.AxisOpts(
                name="用户存量",
                type_="value",
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#d14a61")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            )
        )
            .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value",
                name="用户上线量",
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#675bba")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                name="每日用户增长量",
                position="right",
                offset=80,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#5793f3")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            ),
            title_opts=opts.TitleOpts(title="用户数量"),
            datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=10), opts.DataZoomOpts(type_="inside")],
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        )
    )

    line = (
        Line()
            .add_xaxis(x_data)
            .add_yaxis(
            "每日用户增长量",
            user_increase,
            yaxis_index=2,
            color="#675bba",
            label_opts=opts.LabelOpts(is_show=False),
        )
    )

    bar.overlap(line)
    return Grid().add(
        bar, opts.GridOpts(pos_left="5%", pos_right="20%"), is_control_axis_index=True
    )

# def page_draggable_layout():
#     page = Page(layout=Page.DraggablePageLayout)
#     page.add(
#         bar_datazoom_slider(),
#         line_markpoint(),
#         pie_rosetype(),
#         grid_mutil_yaxis(),
#         liquid_data_precision(),
#         table_base(),
#     )
#     # page.render("page_draggable_layout.html")
#     # tab = Tab()
#     # tab.add(page, "page-example")
#     # tab.render("tab_base.html")
#     # return Markup(page.render_embed())
#     return grid_mutil_yaxis().dump_options()
