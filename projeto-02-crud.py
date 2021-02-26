from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib
import pyodbc
from flask import Flask, jsonify, request

Base = declarative_base()
app = Flask(__name__)

server = 'git090.database.windows.net'
database = 'py_git'
username = 'keymaster'
password = 'm@ravilha1'
driver = '{ODBC Driver 17 for SQL Server}'


conn = ('DRIVER='
        +driver+    
        ';SERVER='  
        +server+    
        ';PORT=1433;DATABASE='  
        +database+  
        ';UID=' 
        +username+  
        ';PWD=' 
        + password)
# pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)


params = urllib.parse.quote_plus(conn)
conn_str = "mssql+pyodbc:///?autocommit=true&odbc_connect={}".format(params)
engine = create_engine(conn_str, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

class APIProject(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price
    
    @property
    def serialize(self):
        return {
            'Name' : self.name,
            'Description' : self.description,
            'Price' : self.price
        }
    
@app.route('/description-product', methods=['POST'])
def create_new_product():
    if request.method == 'POST':
        name = request.args.get('name', '')
        description = request.args.get('description', '')
        price = request.args.get('price', '')

        return add_new_product(name, description, price)

@app.route('/add-product/<string:name>/<string:description>/<int:price>')
def add_new_product(name: str, description: str, price: int):

    Base.metadata.create_all(engine)
    create_product = APIProject(name=name, description=description, price=price)
    session.add(create_product)
    session.commit()

    return jsonify({
        'success' : True,
        'name' : name,
        'description' : description,
        'price' : price
    })






@app.route('/product-delete', methods=['DELETE'])
def delete_product(id: int):
    if request.method == 'DELETE':
        id = request.json.get('id')

        return deleted(id)
    
@app.route('/delete-product/<int:id>')
def deleted(id: int):
    session.query(APIProject).filter(APIProject.id == id).delete()
    success = ' successfully deleted'

    return jsonify({
        'id-product-deleted': str(id) + success
    })

@app.route('/read-all')
def read_all_product():
    return get_all_products()





#GET
@app.route('/get_product/<int:id>')
def get_product(id:int):
    return get_by_product(id)

def get_all_products():
    product = session.query(APIProject).all()
    return jsonify(APIProject=[prod.serialize for prod in product])

def get_by_product(id:int):
    product = session.query(APIProject).filter(APIProject.id == id)
    return jsonify(APIProject=[prod.serialize for prod in product])






@app.route('/alter/<int:id>', methods=['PUT'])
def update(id:int):

    if request.method == 'PUT':
        name = request.json.get('name') 
        description = request.json.get('description')
        price = request.json.get('price')

        return update_product(id, name, description, price)

def update_product(id:int, name:str, description:str, price:float):
    product = session.query(APIProject).filter_by(id=id).first()

    product.name = name
    product.description = description
    product.price = price
    session.commit()

    return jsonify({
        'name': name,
        'description': description,
        'price': price
    })
    

    

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=80)
