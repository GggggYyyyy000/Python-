import numpy as np
import matplotlib.pyplot as plt


category_names = ['超市及大卖场', '日化专营店',
                  '百货专柜', '电商', '其他']
results = {
    '2010': [36.70,14.69,28.6,2.60,17.50],
    '2011': [34.60,15.99,25.80,5.30,18.40],
    '2012': [34.10,16.3,21.80,10.20,17.60],
    '2013': [32.80,16.79,20.50,13.20,16.80],
    '2014': [30.80,17.39,19.60,16.00,16.30],
    '2015': [28.90,17.89,18.80,18.6,15.90],
    '2016': [27.50,18.09,18.50,20.9,15.10],
    '2017': [25.60,18.29,18.80,23.30,14.10],
}

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def survey(results, category_names):
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('Blues')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5,
                label=colname, color=color)
        xcenters = starts + widths / 2

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            ax.text(x, y, str(int(c)), ha='center', va='center',
                    color=text_color)
    ax.set_ylabel('年份',fontsize=12)
    ax.set_xlabel('各渠道占比',fontsize=12)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    return fig, ax


survey(results, category_names)
plt.show()