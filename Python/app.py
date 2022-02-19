from flask import Flask,jsonify,request
from DB import DB

app = Flask(__name__)

@app.route("/update",methods = ['PATCH'])
def update():
    id = int(request.args.get('id'))
    data = request.get_json()
    message = DB().updateEmployeeDetails(ID=id,data=data)
    return message

@app.route('/api')
def api():
    if len(request.args) == 0:
        return jsonify([
            {
                "id":item[0],
                "fname":item[1],
                "lname":item[2],
                "role":item[3]
            }
            for item in DB().getAllEmployeesList()
        ])
    else:
        id = request.args.get('id')
        id = int(id)
        employee = DB().getEmployeeByID(ID=id)
        if len(employee) > 0:
            return jsonify({
                "id":employee[0],
                "fname":employee[1],
                "lname":employee[2],
                "role":employee[3]
                })

@app.route('/delete',methods =['DELETE'])
def delete():
    if len(request.args) > 0:
        message = DB().deleteEmployeeById(ID = request.args.get('id'))
        return message
    else:
        return "Something went wrong"

@app.route('/add',methods=['POST'])
def addEmployee():
    data = request.get_json()
    message = DB().addEmployee(data=data)
    return message

if __name__ == '__main__':
    app.run(debug=True)
