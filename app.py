"""
from flask import Flask
import tabula
import PyPDF2
import urllib.request
import io
import json

app = Flask(__name__)
"""

# -*- coding: utf-8 -*-
from flask import Flask, request, url_for, jsonify

import tabula
import PyPDF2
import urllib.request
import io
import json
app = Flask(__name__)


notes = {
    0: 'do the shopping',
    1: 'build the codez',
    2: 'paint the door',
}


def learnPdfFrutasOutputJson():
    pdf_frutas = "https://files.ceasa-ce.com.br/unsima/boletim_diario/tiangua/frutas_tia.pdf"

    data_frutas = tabula.read_pdf(
        pdf_frutas, output_format="json", pages='all')
    return data_frutas[0]['data']


def learnPdfHortalicasOutputJson():
    pdf_frutas = "https://files.ceasa-ce.com.br/unsima/boletim_diario/tiangua/hortalicas_tia.pdf"

    data_frutas = tabula.read_pdf(
        pdf_frutas, output_format="json", pages='all')
    return data_frutas[0]['data']


def pegarData():
    URL = 'https://files.ceasa-ce.com.br/unsima/boletim_diario/tiangua/frutas_tia.pdf'

    req = urllib.request.Request(URL, headers={'User-Agent': "Magic Browser"})
    remote_file = urllib.request.urlopen(req).read()
    remote_file_bytes = io.BytesIO(remote_file)
    pdfdoc_remote = PyPDF2.PdfFileReader(remote_file_bytes)
    p = pdfdoc_remote.getPage(0)
    text = p.extractText()
    pos = text.find('BOLETIM')
    strdate = text[pos:pos+43]
    test = strdate.split()
    dia = test[4]
    separa = test[5].split('/')
    dia = dia + separa[0]
    mes = separa[1]
    ano = separa[2]
    return dia + '/' + mes + '/' + ano


def retornaJson():
    text = []
    data = []
    i = 0

    for texto in learnPdfFrutasOutputJson():

        i += 1
        text.append({
            "id": i, "nome": texto[0]['text'], 'und': texto[1]['text'], 'sit': texto[2]['text'], 'min': texto[3]['text'], 'mc': texto[4]['text'], 'max': texto[5]['text'], 'procedencia': texto[6]['text']})

    return json.dumps(text)


def retornaJsonHortalicas():
    text = []
    data = []
    i = 0

    for texto in learnPdfHortalicasOutputJson():

        i += 1
        text.append({
            "id": i, "nome": texto[0]['text'], 'und': texto[1]['text'], 'sit': texto[2]['text'], 'min': texto[3]['text'], 'mc': texto[4]['text'], 'max': texto[5]['text'], 'procedencia': texto[6]['text']})

    text.pop(0)
    return json.dumps(text)


def retornaCotacaoPrecoMorango():
    text = []
    i = 0

    for texto in learnPdfFrutasOutputJson():

        i += 1
        text.append({
            "id": i, "nome": texto[0]['text'], 'und': texto[1]['text'], 'sit': texto[2]['text'], 'min': texto[3]['text'], 'mc': texto[4]['text'], 'max': texto[5]['text'], 'procedencia': texto[6]['text']})

    return json.dumps(text[74])


def retornaCotacaoPrecoPimentacao():
    text = []
    data = []
    i = 0

    for texto in learnPdfHortalicasOutputJson():

        i += 1
        text.append({
            "id": i, "nome": texto[0]['text'], 'und': texto[1]['text'], 'sit': texto[2]['text'], 'min': texto[3]['text'], 'mc': texto[4]['text'], 'max': texto[5]['text'], 'procedencia': texto[6]['text']})

    text.pop(0)
    pimentao = []
    j = 72
    while(j < 77):
        pimentao.append(text[j])
        j += 1
    return json.dumps(pimentao)


def retornaCotacaoPrecoTomate():
    text = []
    data = []
    i = 0

    for texto in learnPdfHortalicasOutputJson():

        i += 1
        text.append({
            "id": i, "nome": texto[0]['text'], 'und': texto[1]['text'], 'sit': texto[2]['text'], 'min': texto[3]['text'], 'mc': texto[4]['text'], 'max': texto[5]['text'], 'procedencia': texto[6]['text']})

    text.pop(0)
    tomate = []
    j = 86
    while(j < 95):
        tomate.append(text[j])
        j += 1
    return json.dumps(tomate)


@app.route('/')
def main():
    return ""


@app.route('/api/cotacaoFrutas', methods=['GET'])
def cotacaoFrutas():
    return retornaJson()


@app.route('/api/cotacaoHortalicas', methods=['GET'])
def cotacaoHortalicas():
    return retornaJsonHortalicas()


lista = [
    {
        "id": u'1',
        "plat": u'pc',
        'Nome': u'BFV',
        'Preco': u'250'
    },
    {
        'id': u'2',
        'plataforma': u'mobile',
        'Nome': u'GTA',
        'Preco': u'5000',
    }
]


@app.route('/api/cotacaoMorango', methods=['GET'])
def cotacaoMorangoJson():

    return retornaCotacaoPrecoMorango()
   # return jsonify({'lista':[lista]})


@app.route('/api/cotacaoPimentao', methods=['GET'])
def cotacaoPimentaoJson():
    return retornaCotacaoPrecoPimentacao()


@app.route('/api/cotacaoTomate', methods=['GET'])
def cotacaoTomateJson():
    return retornaCotacaoPrecoTomate()


@app.route('/api/data', methods=['GET'])
def retornaDate():
    return jsonify({"data": pegarData()})


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
