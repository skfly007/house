import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.font_manager import FontProperties
# =====================================================
# SVG文字保留为文本，不转path
# =====================================================
plt.rcParams['svg.fonttype'] = 'none'
# =====================================================
# 中文字体
# =====================================================
font = FontProperties(
    fname="/System/Library/Fonts/STHeiti Light.ttc"
)
# =====================================================
# 文件
# =====================================================
province_file = "中国行政区划地图/天地图_geojson/中国_省.geojson"
city_file = "中国行政区划地图/天地图_geojson/中国_市.geojson"
county_file = "中国行政区划地图/天地图_geojson/中国_县.geojson"
# =====================================================
# 读取GeoJSON
# =====================================================
provinces = gpd.read_file(
    province_file
)
provinces = provinces[
    provinces["name"] != "境界线"
]
cities = gpd.read_file(
    city_file
)
cities = cities[
    cities["name"] != "境界线"
]
counties = gpd.read_file(
    county_file
)
counties = counties[
    (counties["name"] != "境界线")
    &
    (counties.geometry.geom_type.isin(["Polygon","MultiPolygon"]))
]
print("省字段:")
print(provinces.columns)
print("\n地字段:")
print(cities.columns)
print("\n县字段:")
print(counties.columns)
# =====================================================
# 名称字段
# =====================================================
def get_name(row):
    for k in [
        "name",
        "NAME",
        "NL_NAME_1"
    ]:
        if k in row and row[k]:
            return str(row[k])
    return ""
# =====================================================
# 颜色
# =====================================================
colors = {
    # 东北
    "黑龙江省": "#FF9999",
    "吉林省": "#99DDCC",
    "辽宁省": "#CC99FF",
    # 华北
    "内蒙古自治区": "#99BBDD",
    "河北省": "#FFBB88",
    "山西省": "#FFCC66",
    "北京市": "#99CCFF",
    "天津市": "#99DDDD",
    # 西北
    "新疆维吾尔自治区": "#88CCFF",
    "西藏自治区": "#DDA0DD",
    "青海省": "#FFD699",
    "甘肃省": "#FFAAAA",
    "宁夏回族自治区": "#99DDCC",
    "陕西省": "#99EEAA",
    # 华东
    "山东省": "#99BBDD",
    "江苏省": "#99DDDD",
    "浙江省": "#66BBEE",
    "安徽省": "#99AAEE",
    "福建省": "#88DD99",
    "江西省": "#FF9999",
    "上海市": "#FFD699",
    # 华中
    "河南省": "#CC99EE",
    "湖北省": "#99DDCC",
    "湖南省": "#FF9999",
    # 华南
    "广东省": "#FFCC88",
    "广西壮族自治区": "#88CCCC",
    "海南省": "#88DD99",
    "香港特别行政区": "#BB99EE",
    "澳门特别行政区": "#99CC77",
    "台湾省": "#AA99EE",
    # 西南
    "四川省": "#88EEAA",
    "重庆市": "#FFAA88",
    "贵州省": "#FFBB88",
    "云南省": "#99AACC"
}
def province_color(name):
    return colors.get(
        name,
        "#CCCCCC"
    )
# =====================================================
# 创建画布
# =====================================================
fig, ax = plt.subplots(
    figsize=(12,10),
    dpi=300
)
# =====================================================
# 绘制省
# =====================================================
for idx,row in provinces.iterrows():
    name = get_name(row)
    # 省色块
    gpd.GeoSeries(
        [row.geometry],
        crs=provinces.crs
    ).plot(
        ax=ax,
        color=province_color(name),
        edgecolor="black",
        linewidth=0.2
    )
    # 标注点
    p = row.geometry.representative_point()
    ax.text(
        p.x,
        p.y,
        name,
        fontsize=3,
        fontproperties=font,
        ha="center",
        va="center",
        color="#222",
    )
# =====================================================
# 绘制市界
# =====================================================
cities.boundary.plot(
    ax=ax,
    color="black",
    linewidth=0.1
)
# =====================================================
# 绘制市名称
# =====================================================
for idx,row in cities.iterrows():
    name = get_name(row)
    p = row.geometry.representative_point()
    ax.text(
        p.x,
        p.y,
        name,
        fontsize=1.1,
        fontproperties=font,
        ha="center",
        va="center",
        color="#444",
    )

# =====================================================
# 绘制县界
# =====================================================

counties.boundary.plot(
    ax=ax,
    color="#666666",
    linewidth=0.03
)
# =====================================================
# 绘制县名称
# =====================================================

for idx, row in counties.iterrows():

    name = get_name(row)

    p = row.geometry.representative_point()

    ax.text(
        p.x,
        p.y,
        name,
        fontsize=0.1,
        fontproperties=font,
        ha="center",
        va="center",
        color="#666666",
    )
# =====================================================
# 去掉坐标轴
# =====================================================
ax.axis("off")
plt.tight_layout()
# =====================================================
# 输出SVG
# =====================================================
plt.savefig(
    "中国行政区地图.svg",
    format="svg",
    bbox_inches="tight"
)
plt.close()

import re

with open("中国行政区地图.svg", "r", encoding="utf-8") as f:
    svg = f.read()

# 把 fill:#666666 的文字字体改成 0.5px
svg = re.sub(
    r'font-size:\s*1px;([^"]*?)fill:\s*#666666',
    r'font-size:0.5px;\1fill:#666666',
    svg
)

with open("中国行政区地图.svg", "w", encoding="utf-8") as f:
    f.write(svg)


print(
    "生成完成: 中国行政区地图.svg"
)

