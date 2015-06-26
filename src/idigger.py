#!/usr/bin/env python2.7

from __future__ import print_function

import os.path
import datetime

# activate pre-installed virtual environment containing the libraries;
# in other words, run from $HOME
this_file = "idigger/src/venv/bin/activate_this.py"
execfile(this_file, dict(__file__=this_file))

from flask import Flask, jsonify, abort, make_response, request
from flask.ext.cors import CORS
from flask.ext.sqlalchemy import SQLAlchemy

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

@app.route('/api/v0.1/snapshot/<string:date>', methods=['GET'])
def get_snapshot(date):
    def get_workday(d):
        """
        Returns the friday before if the date requested is on weekend.
        BM&FBovespa do not operate on these days and it's wise to not
        run fetcher on these, to save size on database.
        """

        if d.weekday() == 5:
            return d - datetime.timedelta(days=1)
        elif d.weekday() == 6:
            return d - datetime.timedelta(days=2)
        else:
            return d

    # the reference snapshot
    try:
        # no strptime() in date object, so we need to date()
        d = datetime.datetime.strptime(date, '%Y%m%d').date()
    except ValueError:
        return make_response(jsonify( \
                {'error': 'invalid date format'}), 404)

    wd = get_workday(d)
    query1 = Stock.query. \
            filter_by(date=wd). \
            order_by(Stock.gb_eyroc_order). \
            limit(20). \
            all()

    today = get_workday(datetime.date.today())

    top = []
    snapshot_gain = []

    # for each stock from the snapshot
    # and build the response
    for q in query1:
        pc1 = q.pc

        query2 = Stock.query.filter_by(code=q.code, date=today).first()
        try:
            pc2 = query2.pc
        except AttributeError:
            return make_response(jsonify( \
                    {'error': 'no data available for today'}), 404)

        gain = ((pc2 - pc1) / pc1) * 100
        snapshot_gain.append(gain)

        top.append([q.code, gain])

    try:
        gain = sum(snapshot_gain)/len(snapshot_gain)
    except ZeroDivisionError:
        return make_response(jsonify( \
                {'error': 'no data for this snapshot'}), 404)

    resp = { 'stocks': top, 'gain': sum(snapshot_gain)/len(snapshot_gain) }
    return jsonify(resp)

@app.route('/api/v0.1/stock/all', methods=['GET'])
def get_stocks_today():
    d = datetime.date.today()
    query = Stock.query.filter_by(date=d).all()
    s = {}

    for q in query:
        s[q.code] = { \
                'code': q.code, \
                'ey': q.ey, \
                'roc': q.roc, \
                'pe': q.pe, \
                'roe': q.roe, \
                'pc': q.pc, \
                'gb_eyroc_order': q.gb_eyroc_order \
                }

    return jsonify(s)

@app.route('/api/v0.1/test', methods=['GET'])
def get_test():
    s = { 'list': ['foo', 'bar', 'a'] }

    return jsonify(s)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'not found'}), 404)

# development only, do not need this with Tornado
if __name__ == '__main__':
    #app.run(debug = True, use_reloader = False)
    app.run(debug = True)
