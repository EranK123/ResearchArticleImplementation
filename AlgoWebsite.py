from flask import Flask, redirect, url_for, render_template, request
from wtforms import URLField, StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
import contiguous_oriented_labeling
import PiecewiseConstantValuation as pc
import proportional_cake_allocation as pca
import ast
import networkx as nx

app = Flask(__name__)


class Input(FlaskForm):
    agent1_valuations = StringField(label="Agent 1 Valuations", validators=[DataRequired()])
    agent2_valuations = StringField(label="Agent 2 Valuations", validators=[DataRequired()])
    graph = StringField(label="Edges of the graph", validators=[DataRequired()])
    submit = SubmitField(label="Get Valuations")


class Return(FlaskForm):
    b = SubmitField(label="Return")


@app.route("/results", methods=['GET', 'POST'])
def algo_results():
    b = Return()
    if b.is_submitted():
        return redirect(url_for(home.__name__))
    return render_template("results.html", results=algo_results.results, b=b)


@app.route("/", methods=['GET', 'POST'])
def home():
    form = Input()
    submit = form.validate_on_submit()
    if not submit:
        return render_template("home.html", form=form)
    agent1_vals = [stringlist_to_intlist(val) for val in form.agent1_valuations.data.split(' ')]
    agent2_vals = [stringlist_to_intlist(val) for val in form.agent2_valuations.data.split(' ')]
    graph_edges = [stringlist_to_intlist(val) for val in form.graph.data.split(' ')]
    piecewise_agent1 = []
    for i in agent1_vals:
        piecewise_agent1.append(pc.PiecewiseConstantValuation(i))
    piecewise_agent2 = []
    for i in agent2_vals:
        piecewise_agent2.append(pc.PiecewiseConstantValuation(i))
    g = nx.Graph()
    print(graph_edges)
    g.add_edges_from(graph_edges)
    g1, g2 = pca.get_proportional_allocation(piecewise_agent1, piecewise_agent2, g)
    g1_info = []
    g2_info = []
    for edge in g1.edges:
        g1_info.append((edge, g1.get_edge_data(edge[0], edge[1])))
    for edge in g2.edges:
        g2_info.append((edge, g2.get_edge_data(edge[0], edge[1])))
    algo_results.results = [g1_info, g2_info]
    return redirect(url_for(algo_results.__name__))


def stringlist_to_intlist(str_list):
    res = ast.literal_eval(str_list)
    return res


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'fnehauildagsukl'
    app.run(debug=True, host='0.0.0.0', port=5555)
