from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient()
db = client.Hedgerow
investments = db.investments

app = Flask(__name__)

# home/investment route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/')
def investments_index():
  ''' Show all investments '''
  return render_template('investments_index.html', investments=investments.find())

# new investment form route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/investments/new')
def investments_new():
  ''' Create a new investment '''
  investment = {
    'title': 'title',
    'description': 'description',
    'amount': 'amount'
  }
  return render_template('investments_new.html', title='New Investment', investment=investment)

# investments post request route ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
# submit route for investments post request form dict info to be added as an investment object in the database
@app.route('/investments', methods=['POST'])
def investments_submit():
  ''' Submit a new investment '''
  investment = {
    'title': request.form.get('title'),
    'description': request.form.get('description'),
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
  return render_template('investments_edit.html', investment=investment, title='Edit investment')

# Update route for single investments ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~
@app.route('/investments/<investment_id>', methods=['POST'])
def investments_update(investment_id):
  ''' Submit an edited investment '''
  updated_investment = {
    'title': request.form.get('title'),
    'description': request.form.get('description'),
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

if __name__ == '__main__':
  app.run(debug=True)