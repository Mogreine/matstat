import numpy as np
from scipy.stats import chi2, norm
import plotly.graph_objs as go
import plotly


def gen_sample(n, sigma):
    return np.random.normal(0, sigma, n)


def st1(samp: np.ndarray):
    gamma = 0.95
    sq_sum = np.sum(samp ** 2)
    left_quantile = chi2.ppf((1 + gamma) / 2, len(samp))
    right_quantile = chi2.ppf((1 - gamma) / 2, len(samp))

    l = sq_sum / left_quantile
    r = sq_sum / right_quantile

    return l, r


def st2(samp: np.ndarray):
    gamma = 0.99
    m = np.mean(samp)
    n = len(samp)

    left_quantile = norm.ppf((3 + gamma) / 4)
    right_quantile = norm.ppf((3 - gamma) / 4)

    l = n * m ** 2 / left_quantile ** 2
    r = n * m ** 2 / right_quantile ** 2

    return l, r


def test_stat(sigma, st, l, r, step):
    l_arr, r_arr, sig, x = [], [], [], []
    for i in range(l, r + 1, step):
        sample = gen_sample(i, sigma)
        sigma_l, sigma_r = st(sample)

        x.append(i)
        l_arr.append(sigma_l)
        r_arr.append(sigma_r)
        sig.append(sigma ** 2)
    return l_arr, r_arr, sig, x


def plot(*data):
    traces = []
    x = data[-1]
    colors = [
        {'color': 'rgba(0, 255, 0, 0.8)'},
        {'color': 'rgba(255, 0, 0, 0.8)'},
        {'color': 'rgba(0, 0, 0, 0.8)'},
    ]
    names = [
        'left',
        'right',
        f'$\sigma^2$'
    ]
    for i in range(len(data) - 1):
        traces.append(go.Scatter(
            x=x,
            y=data[i],
            mode='lines+markers',
            marker=colors[i],
            name=names[i]
        ))

    layout = go.Layout(
        title={
            'text': "Зависимость границ интервала от размера выборки",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis={
            'title': 'n'
        },
        yaxis={
            'title': f'$\sigma^2$'
        }
    )
    fig = go.Figure(data=traces, layout=layout)
    plotly.offline.iplot(fig)


sigma = 10
n = 1000000
sample = gen_sample(n, sigma)

print(sigma)
print(st1(sample))

data = test_stat(sigma, st2, 100, 10000, 50)
plot(*data)
