from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient()
db = client.Hedgerow
investments = db.investments
assets = db.assets

app = Flask(__name__)

# home route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/')
def home_index():
  ''' Show home page '''
  return render_template('home_index.html')

# INVESTMENTS RESOURCE & ROUTES ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
# investments route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/investments')
def investments_index():
  ''' Show all investments '''
  return render_template('investments_index.html', investments=investments.find())

# new investment form route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/investments/new')
def investments_new():
  ''' Create a new investment '''
  investment = {
    'asset': 'asset',
    'amount': 'amount'
  }
  return render_template('investments_new.html', title='New Investment', investment=investment, assets=assets.find())

# investments post request route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
# submit route for investments post request form dict info to be added as an investment object in the database
@app.route('/investments', methods=['POST'])
def investments_submit():
  ''' Submit a new investment '''
  investment = {
    'asset': request.form.get('asset'),
    'amount': '$' + request.form.get('amount')
  }
  investment_id = investments.insert_one(investment).inserted_id
  return redirect(url_for('investments_show', investment_id=investment_id))

# single investment route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/investments/<investment_id>')
def investments_show(investment_id):
  ''' Show a single investment '''
  investment = investments.find_one({'_id': ObjectId(investment_id)})
  return render_template('investments_show.html', investment=investment)

# Edit route for single investments ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/investments/<investment_id>/edit')
def investments_edit(investment_id):
  ''' Edit a single investment '''
  investment = investments.find_one({'_id': ObjectId(investment_id)})
  return render_template('investments_edit.html', investment=investment, assets=assets.find(), title='Edit investment')

# Update route for single investments ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/investments/<investment_id>', methods=['POST'])
def investments_update(investment_id):
  ''' Submit an edited investment '''
  updated_investment = {
    'asset': request.form.get('asset'),
    'amount': '$' + request.form.get('amount')
  }
  investments.update_one(
    {'_id': ObjectId(investment_id)},
    {'$set': updated_investment}
  )
  return redirect(url_for('investments_show', investment_id=investment_id))

# Delete route for single investments ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/investments/<investment_id>/delete', methods=['POST'])
def investments_delete(investment_id):
  ''' Delete one investment '''
  investments.delete_one({'_id': ObjectId(investment_id)})
  return redirect(url_for('investments_index'))
# ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~~-~-~-~-~-~-~-~-~-~-~-~-~-~-~

# ASSETS RESOURCE & ROUTES ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~~-~-~
# assets route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/assets')
def assets_index():
  ''' Show all assets '''
  return render_template('assets_index.html', assets=assets.find())

# new asset form route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/assets/new')
def assets_new():
  ''' Create a new asset '''
  asset = {
    'title': 'title',
    'description': 'description',
    'reason': 'reason'
  }
  return render_template('assets_new.html', title='New Asset', asset=asset)

# assets post request route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
# submit route for assets post request form dict info to be added as an asset object in the database
@app.route('/assets', methods=['POST'])
def assets_submit():
  ''' Submit a new asset '''
  asset = {
    'title': request.form.get('title'),
    'description': request.form.get('description'),
    'reason': request.form.get('reason')
  }
  asset_id = assets.insert_one(asset).inserted_id
  return redirect(url_for('assets_show', asset_id=asset_id))

# single investment route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/assets/<asset_id>')
def assets_show(asset_id):
  ''' Show a single asset '''
  asset = assets.find_one({'_id': ObjectId(asset_id)})
  return render_template('assets_show.html', asset=asset)

# Edit route for single investments ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/assets/<asset_id>/edit')
def assets_edit(asset_id):
  ''' Edit a single asset '''
  asset = assets.find_one({'_id': ObjectId(asset_id)})
  return render_template('assets_edit.html', asset=asset, title='Edit asset')

# Update route for single assets ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/assets/<asset_id>', methods=['POST'])
def assets_update(asset_id):
  ''' Submit an edited asset '''
  updated_asset = {
    'title': request.form.get('title'),
    'description': request.form.get('description'),
    'reason': request.form.get('reason')
  }
  assets.update_one(
    {'_id': ObjectId(asset_id)},
    {'$set': updated_asset}
  )
  return redirect(url_for('assets_show', asset_id=asset_id))

# Delete route for single investments ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/assets/<asset_id>/delete', methods=['POST'])
def assets_delete(asset_id):
  ''' Delete one asset '''
  assets.delete_one({'_id': ObjectId(asset_id)})
  return redirect(url_for('assets_index'))


if __name__ == '__main__':
  app.run(debug=True)