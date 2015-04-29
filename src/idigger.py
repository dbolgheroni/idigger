#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012-2015, Daniel Bolgheroni. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
# 
# THIS SOFTWARE IS PROVIDED BY DANIEL BOLGHERONI ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL DANIEL BOLGHERONI OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from flask import Flask, jsonify, abort, make_response, request
from flask.ext.cors import CORS
from flask.ext.sqlalchemy import SQLAlchemy
import os.path
import time
import datetime

from conf import dbfile

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
cors = CORS(app)
db = SQLAlchemy(app)


class Stock(db.Model):
    __tablename__ = 'stocks'
    date = db.Column(db.Date, primary_key = True)
    code = db.Column(db.String, primary_key = True)
    ey = db.Column(db.Float)
    roc = db.Column(db.Float)
    pe = db.Column(db.Float)
    roe = db.Column(db.Float)
    pc = db.Column(db.Float)

    ey_order = db.Column(db.Integer)
    roc_order = db.Column(db.Integer)
    gb_eyroc_order = db.Column(db.Integer)

    pe_order = db.Column(db.Integer)
    roe_order = db.Column(db.Integer)
    gb_peroe_order = db.Column(db.Integer)

    def __repr__(self):
        return '<Stock %r>' % (self.code)

@app.route('/api/v0.1/stock/<string:stock>', methods=['GET'])
def get_stock(stock):
    s = Stock.query.filter_by(code=stock).first_or_404()
    sresp = {
            'code': s.code,
            'ey': s.ey,
            'roc': s.roc,
            'pe': s.pe,
            'roe': s.roe }

    return jsonify(sresp)

@app.route('/api/v0.1/stocks/today', methods=['GET'])
def get_stocks_today():
    d = datetime.date.today()
    query = Stock.query.filter_by(date=d).all()
    s = {}

    for q in query:
        s[q.code] = { 'code': q.code, 'ey': q.ey, 'roc': q.roc,
                'pe': q.pe, 'roe': q.roe, 'pc': q.pc,
                'gb_peroe_order': q.gb_peroe_order,
                'gb_eyroc_order': q.gb_eyroc_order }

    return jsonify(s)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'not found'}), 404)

#def get_tasks():
#    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    #app.run(debug = True, use_reloader = False)
    app.run(debug = True)
