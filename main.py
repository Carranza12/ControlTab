from flask import Flask
# https://codepen.io/PrabuDzak/pen/ygRaGW    Simple DXF viewer
# https://www.youtube.com/watch?v=_YeN69XoqqU
# https://www.digitalocean.com/community/tutorials/how-to-generate-a-vue-js-single-page-app-with-vue-create
# https://www.freecodecamp.org/news/the-vue-handbook-a-thorough-introduction-to-vue-js-1e86835d8446/
# 
from dbconect import *
from flask import jsonify, request, render_template, redirect

app = Flask(__name__)

db_psql = psql_db_interface('dbmaquinas')

@app.route('/')
def main(): # For default route
    machines = []
    try:
       rows = db_psql.execute_query("SELECT id, nombre, modelo, categoria, precio, marca, dimensiones, material_que_procesa, operacion, vendedor, potencia FROM public.maquinas")
       for row in rows:
           machines.append({"id": row[0], "nombre": row[1], "modelo": row[2], "categoria": row[3], "precio": row[4], "marca": row[5], "dimensiones": row[6], "material_que_procesa": row[7], "operacion": row[8], "vendedor": row[9], "potencia": row[10]})
    except Exception as e:
       print(e)

    return render_template('machineslist.html', machines = machines)

@app.route('/details/<int:id>', methods=['GET'])
def user_details(id):
    [rslt] = db_psql.execute_query_with_param("select * from public.maquinas where id = %s", (id,))
    return render_template('details.html', rslt=rslt)

@app.route('/add', methods=['GET','POST'])
def add_user():
    if request.method == 'GET':
        return render_template("add.html", rslt=(None, "", "", ""))
    _nombre = request.form['nombre']
    _modelo = request.form['modelo']
    _categoria = request.form['categoria']
    _precio = request.form['precio']
    _marca = request.form['marca']
    _dimensiones = request.form['dimensiones']
    _material_que_procesa = request.form['material_que_procesa']
    _operacion = request.form['operacion']
    _vendedor = request.form['vendedor']
    _potencia = request.form['potencia']
    
    # validate the received values
    if _nombre and _modelo and _categoria and _precio and _marca and _dimensiones and _material_que_procesa  and _operacion  and _vendedor and _potencia and request.method == 'POST':
        sql = "INSERT INTO public.maquinas(nombre, modelo, categoria,precio, marca, dimensiones, material_que_procesa, operacion,vendedor, potencia ) VALUES(%s, %s, %s, %s, %s , %s , %s , %s , %s , %s)"
        data = (_nombre, _modelo, _categoria,_precio, _marca, _dimensiones,_material_que_procesa, _operacion,_vendedor,_potencia)
        db_psql.commit()
        return redirect('/')
    else:
        return not_found()

# @app.route('/users')
# def users():
#     try:
#         rows = db_psql.execute_query("SELECT user_id, user_name, user_email, user_password FROM tbluser")
#         # rows = cursor.fetchall()
#         resp = jsonify(rows)
#         resp.status_code = 200
#         return resp
#     except Exception as e:
#         print(e)

# @app.route('/user/<int:id>')
# def user(id):
#     try:
#         rows = db_psql.execute_query_with_param("SELECT user_id, user_name, user_email, user_password FROM tbluser WHERE user_id=%s", id)
#         row = db_psql.cursor.fetchone()
#         resp = jsonify(row)
#         resp.status_code = 200
#         return resp
#     except Exception as e:
#         print(e)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    if request.method == 'GET':
     [rslt] = db_psql.execute_query_with_param("select * from public.maquinas where id = %s", (id,))
     return render_template("add.html", rslt=rslt)
    _nombre = request.form['nombre']
    _modelo = request.form['modelo']
    _categoria = request.form['categoria']
    _precio = request.form['precio']
    _marca = request.form['marca']
    _dimensiones = request.form['dimensiones']
    _material_que_procesa = request.form['material_que_procesa']
    _operacion = request.form['operacion']
    _vendedor = request.form['vendedor']
    _potencia = request.form['potencia']
    # validate the received values
    if _nombre and _modelo and _categoria and _precio and _marca and _dimensiones and _material_que_procesa  and _operacion  and _vendedor and _potencia and request.method == 'POST':
        #do not save password as a plain text
        # save edits
        sql = "UPDATE public.maquinas SET nombre=%s, modelo=%s, categoria=%, precio=%s ,marca=%s ,dimensiones=%s ,material_que_procesa=%s ,operacion=%s ,vendedor=%s,potencia=%s  WHERE id=%s"
        data = (_nombre, _modelo, _categoria,_precio, _marca, _dimensiones,_material_que_procesa, _operacion,_vendedor,_potencia)
        db_psql.execute_query_nr_with_param(sql, data)
        db_psql.commit()
        return redirect('/')
    else:
        return not_found()

@app.route('/delete/<int:id>', methods=['GET'])
def delete_user(id):
    db_psql.execute_query_nr_with_param("DELETE FROM public.maquinas WHERE id=%s", (id,))
    db_psql.commit()
    return redirect('/')
#
# @app.errorhandler(404)
# def not_found(error=None):
#     message = {
#         'status': 404,
#         'message': 'Not Found: ' + request.url,
#     }
#     resp = jsonify(message)
#     resp.status_code = 404
#
#     return resp

if __name__ == '__main__':
    app.run(port=50001)

