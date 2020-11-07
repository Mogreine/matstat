import numpy as np
import plotly.graph_objs as go
import plotly


def plot(x, uni, exp):
    trace1 = go.Scatter(
        x=x,
        y=uni,
        mode='lines',
        marker={'color': 'rgba(0, 255, 0, 0.8)'},
        name='uni',
        xaxis='x1',
        yaxis='y1'
    )
    trace2 = go.Scatter(
        x=x,
        y=exp,
        mode='lines',
        marker=dict(color='rgba(255, 0, 0, 0.8)'),
        name='exp',
        xaxis='x2',
        yaxis='y2'
    )
    data = [trace1, trace2]

    layout = go.Layout(
        title='Зависимость std от k',
        xaxis=dict(
            domain=[0, 0.45]
        ),
        yaxis=dict(
            domain=[0, 0.65]
        ),
        xaxis2=dict(
            domain=[0.55, 1]
        ),
        yaxis2=dict(
            domain=[0, 0.65],
            anchor='x2'
        )
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.iplot(fig)


def gen_uni(theta, n=10000):
    return np.random.uniform(0, theta, n)


def gen_exp(theta, n=10000):
    return np.random.exponential(theta, n)


def eval_param_uni(data_k, k):
    return ((k + 1) * np.mean(data_k)) ** (1 / k)


def eval_param_exp(data_k, k):
    return (np.mean(data_k) / np.math.factorial(k)) ** (1 / k)


def eval_std(data_gen_func, eval_func, n, s, k, theta):
    theta_eval_arr = []
    for i in range(1, s + 1):
        data = data_gen_func(theta, n)
        data_k = data ** k
        theta_eval = eval_func(data_k, k)
        theta_eval_arr.append(theta_eval)
    res = std(np.array(theta_eval_arr), theta)
    return res


def std(arr, param):
    return np.sum((arr - param) ** 2) / len(arr)


if __name__ == "__main__":
    uni_theta, exp_theta = 100, 10
    n, s = 1000, 100

    exp_std_arr, uni_std_arr = [], []
    k_arr = [*range(1, 101)]
    for k in k_arr:
        uni_std_k = eval_std(gen_uni, eval_param_uni, n, s, k, uni_theta)
        exp_std_k = eval_std(gen_exp, eval_param_exp, n, s, k, exp_theta)

        uni_std_arr.append(uni_std_k)
        exp_std_arr.append(exp_std_k)

    plot(k_arr, uni_std_arr, exp_std_arr)
