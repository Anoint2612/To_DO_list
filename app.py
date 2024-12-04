from flask import Flask, render_template,redirect,request,url_for
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#MY aPP
app=Flask(__name__)
Scss(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)

class MyTask(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False) #nullable=False means that the field cannot be left in
    complete=db.Column(db.Boolean,default=False) #default=False means that the field is not
    created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr___(self)->str:
        return f"Task {self.id}"
    
@app.route("/",methods=["POST","GET"]) #As it is a decorator, it is used to add a function to the route

def home():
    if request.method=="POST":
        current_task=request.form['task']
        new_task=MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERRROR:{e}"
    #See all current tasks

    else:
        tasks=MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html",tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task=MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    
    except Exception as e:
        return f"ERROR:{e}"
    
#Edit the Task
@app.route("/edit/<int:id>",methods=["POST","GET"])
def edit(id:int):
    task=MyTask.query.get_or_404(id)
    if request.method=="POST":
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR:{e}"
        
    else:
        return render_template("edit.html",task=task)

if __name__ == "__main__":
    app.run(debug=True)