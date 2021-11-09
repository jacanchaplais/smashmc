# -*- coding: utf-8 -*-
"""
Created on Tue 9 Nov 15:59:49 GMT 2021

@author: jacanchaplais
"""

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import visdcc
from colliderscope.plot import ShowerDAG
from heparchy.data import SignalVertex
from heparchy.hepmc import HepMC


app = dash.Dash()
server = app.server

app.layout = html.Div(
        children=[
            visdcc.Network(
                id='net',
                options=dict(height='600px', width='100%', directed=True,)
                ),
            html.Br(),html.Br(),
            html.Label('Provide path for data file to display:'),
            dcc.Input(id='filepath', type='text', placeholder=''),
            html.Br(),html.Br(),
            html.Label('Particles in:'),
            dcc.Input(id='in-pdgs', type='text', placeholder='25'),
            html.Label('Particles out:'),
            dcc.Input(id='out-pdgs', type='text', placeholder='5,-5'),
            html.Br(),html.Br(),
            html.Label('Which event in the file would you like to see?'),
            dcc.Input(id='evt-num', type='number', value=1),
    ])

def sanitise_num_list(num_list):
    if num_list == None:
        return []
    num_list = str(num_list).replace(' ', '')
    if num_list == '':
        return []
    num_list = num_list.split(',')
    num_list = list(map(int, num_list))
    return num_list

@app.callback(Output('net', 'data'), [
        Input('filepath', 'value'),
        Input('in-pdgs', 'value'),
        Input('out-pdgs', 'value'),
        Input('evt-num', 'value'),
        ])
def myfun(filepath, in_pdgs, out_pdgs, evt_num):
    evt_num = int(evt_num)
    with HepMC(filepath) as raw_f:
        for i, event in enumerate(raw_f):
            if i > evt_num:
                break
    in_pdgs = sanitise_num_list(in_pdgs)
    out_pdgs = sanitise_num_list(out_pdgs)
    follow_pdgs = out_pdgs
    signal_vertices = [SignalVertex(incoming=in_pdgs, outgoing=out_pdgs,
                                    follow=follow_pdgs)]
    signal_masks = event.signal_mask(signal_vertices)
    mask_dict = dict()
    count = 0
    for vertex_masks in signal_masks:
        for parton_mask in vertex_masks.values():
            count += 1
            mask_dict[f'mask_{count}'] = parton_mask
    shower_dag = ShowerDAG.from_heparchy(event, masks=mask_dict)

    data = {'nodes': shower_dag._vis_nodes(kamada_kawai=True),
            'edges': shower_dag._vis_edges(),
            }
    return data

if __name__ == '__main__':
    app.run_server(debug=True)
