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
        title={
            # 'text': "$\theta_{uni} = 20,\; \theta_{exp} = 10$",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis1=dict(
            domain=[0, 0.45],
            title='k'
        ),
        xaxis2=dict(
            domain=[0.55, 1],
            title='k'
        ),
        yaxis1=dict(
            anchor='x1',
            title='mse',
            showexponent='all',
            exponentformat='e'
        ),
        yaxis2=dict(
            anchor='x2',
            title='mse',
            showexponent='all',
            exponentformat='e'
        )
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.iplot(fig)


def gen_uni(theta, n=1000):
    return np.random.uniform(0, theta, n)


def gen_exp(theta, n=1000):
    return np.random.exponential(theta, n)


def eval_param_uni(data_k, k):
    return ((k + 1) * np.mean(data_k)) ** (1 / k)


def eval_param_exp(data_k, k):
    return (np.mean(data_k) / np.math.factorial(k)) ** (1 / k)


def eval_mse(data_gen_func, eval_func, n, s, k, theta):
    theta_eval_arr = []
    for i in range(1, s + 1):
        data = data_gen_func(theta, n)
        data_k = data ** k
        theta_eval = eval_func(data_k, k)
        theta_eval_arr.append(theta_eval)
    res = mse(np.array(theta_eval_arr), theta)
    return res


def mse(arr, param):
    e = arr - param
    return e @ e / len(e)


def calc(uni_theta, exp_theta, n=1000, s=100):
    exp_mse_arr, uni_mse_arr = [], []
    k_arr = [*range(1, 101)]
    for k in k_arr:
        uni_mse_k = eval_mse(gen_uni, eval_param_uni, n, s, k, uni_theta)
        exp_mse_k = eval_mse(gen_exp, eval_param_exp, n, s, k, exp_theta)

        uni_mse_arr.append(uni_mse_k)
        exp_mse_arr.append(exp_mse_k)

    plot(k_arr, uni_mse_arr, exp_mse_arr)


if __name__ == "__main__":
    calc(20, 20)
