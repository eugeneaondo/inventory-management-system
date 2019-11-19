from flask import Flask,render_template,request,redirect,url_for
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from configs.configs import Development
import pygal

app = Flask(__name__)

app.config.from_object(Development)
#instance of SQLALCHEMY
db = SQLAlchemy(app)
from models.inventories import InventoryModel
from models.sales import SalesModel
@app.before_first_request
def create_tables():
    db.create_all()
    # db.drop_all()

@app.route('/')
def hello_world():
    pie_chart = pygal.Pie()
    pie_chart.title = 'Products and Services'
    pie_chart.add('Products',InventoryModel.getTypeCount("Product"))
    pie_chart.add('Goods', InventoryModel.getTypeCount("Goods"))
    pie_type = pie_chart.render_data_uri()
    return render_template("index.html", pie_type=pie_type)

@app.route('/line')
def line_graph():
    # graph = pygal.Line()
    # graph.title = '% Change of sales over time.'
    # graph.x_labels = ['2011', '2012', '2013', '2014', '2015', '2016']
    # graph.add('Python', [15, 31, 89, 200, 356, 900])
    # graph.add('Java', [15, 45, 76, 80, 91, 95])
    # graph.add('C++', [5, 51, 54, 102, 150, 201])
    # graph.add('All others combined!', [5, 15, 21, 55, 92, 105])
    # graph_data = graph.render_data_uri()
    # return render_template("linegraph.html", graph_data=graph_data)

    conn = psycopg2.connect("dbname='ecommerce' user='postgres' host='localhost' password='postgres'")

    cur = conn.cursor()
    cur.execute("""Select (sum(i.bp * s.qyt)) as subtotal,(Extract(month FROM s.time_created)) as sales_month 
from sales as s
join inventories as i on s.inv_id = i.id
group by sales_month
order by sales_month""")
    rows = cur.fetchall()
    x=[]
    y=[]
    for row in rows:
        x.append(row[1])
        y.append(row[0])
    line= pygal.Radar()
    line.title = '% Change of sales over time.'
    line.x_labels = x
    line.add('Subtitle',y)
    line_data = line.render_data_uri()
    return render_template('linegraph.html',line_data=line_data)


@app.route('/line')
def bar():
    conn = psycopg2.connect("dbname='ecommerce' user='postgres' host='localhost' password='postgres'")
    cur = conn.cursor()
    cur.execute("""Select (sum(i.bp * s.qyt)) as subtotal,(Extract(month FROM s.time_created)) as sales_month 
from sales as s
join inventories as i on s.inv_id = i.id
group by sales_month
order by sales_month""")
    rows=cur.fetchall()
    x=[]
    y=[]
    for row in rows:
        x.append(row[1])
        y.append(row[0])

    bar= pygal.Bar()
    bar.title = 'sales bar graph '
    bar.x_labels = x
    bar.add('subtitle', y)
    line_bar=bar.render_data_uri()
    return render_template('linegraph.html',line_bar=line_bar)

@app.route('/inventories', methods=['GET','POST'])
def inventories():
    x = InventoryModel.query.all()

    if request.method == 'POST':

        name = request.form['name']
        types = request.form['types']
        buying_price = request.form['bp']
        selling_price = request.form['sp']
        stock= request.form['stock']
        reorder= request.form['reorder']

        # print(name)
        # print(types)
        # print(buying_price)
        # print(selling_price)
        # print(stock)
        # print(reorder)
        obj=InventoryModel(invname=name,invtype=types,bp=buying_price,sp=selling_price,stock=stock,rp=reorder)
        db.session.add(obj)
        db.session.commit()
        print("success")
        return redirect(url_for('inventories'))
    return render_template('inv.html',inventories=x)

@app.route('/sales', methods=['GET','POST'])
def sales():
    if request.method == 'POST':
        quantity = request.form['quantity']
        forkey = request.form['forkey']
        print(quantity)
        InventoryModel.updatestock(forkey,int(quantity))
        save=SalesModel(inv_id=forkey,qyt= quantity)
        db.session.add(save)
        db.session.commit()

        return redirect(url_for('inventories'))

@app.route('/inventory/<int:id>/sale')
def view_sales(id):
    inv=InventoryModel.query.filter_by(id=id).first()
    # list of sales
    sales_inv=inv.sales
    return render_template('sales.html',sales=sales_inv)

@app.route('/edit', methods=['GET','POST'])
def edit():

    if request.method == 'POST':
        inv_id = request.form['id']
        name = request.form['name']
        types = request.form['types']
        buying_price = request.form['bp']
        selling_price = request.form['sp']
        stock= request.form['stock']
        reorder= request.form['reorder']

        InventoryModel.editstock(id=inv_id,chname=name,chtype=types,chbp=buying_price,chsp=selling_price,chstock=stock,chreoder=reorder)
        return redirect(url_for('inventories'))


@app.route('/about')
def about():
    return render_template('about.html')



# @app.route('/delete', method=['GET','POST'])
# def delete():
#     if request.method == 'POST':
#         pass
#     # print(quantity)
#
#     # db.session.delete()
#     # db.session.commit()

if __name__ == '__main__':
    app.run()
