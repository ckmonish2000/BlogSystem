from flask import Flask,render_template,url_for,request,redirect
from sqlalchemy import create_engine,MetaData,Table,Column,Integer,String


engine = create_engine('sqlite:///blogpost.db', echo = True)
meta=MetaData()
conn=engine.connect()

blog=Table(
    "blog",meta,
    Column("id",Integer,primary_key=True),
    Column("author",String),
    Column("content",String)
)

meta.create_all(engine)


# insert=blog.insert().values(author="mk",content="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
# exe=conn.execute(insert)
# print(str(exe))
# x=blog.select()
# y=conn.execute(x)
# z=y.fetchall()
# for zz in z:
#     print(zz)

app=Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/post",methods=["GET","POST"])
def post():
    if request.method=="POST":
        auth=request.form.get("author")
        contents=request.form.get("content")
        insert=blog.insert().values(author=auth,content=contents)
        conn=engine.connect()
        exe=conn.execute(insert)
        return "<h1 class=\"heading\">Uploaded Content</h1>"
    return render_template("post.html")


@app.route("/blog")
def blogs():
    conn=engine.connect()
    gets=blog.select()
    exe=conn.execute(gets)
    result=exe.fetchall()
    return render_template("blog.html",posts=result)


@app.route("/view/<int:num>")
def view(num):
    conn=engine.connect()
    gets=blog.select().where(blog.c.id==num)
    print(gets)
    exe=conn.execute(gets)
    result=exe.fetchall()
    return render_template("view.html",data=result)



@app.route("/delete/<int:num>")
def delete(num):
    conn=engine.connect()
    dell=blog.delete().where(blog.c.id==num)
    conn.execute(dell)
    return redirect(url_for("blogs"))



@app.route("/update/<int:num>",methods=["GET","POST"])
def update(num):
    conn=engine.connect()
    if request.method=="POST":
        auth=request.form.get("author")
        cont=request.form.get("content")
        updation=blog.update().where(blog.c.id==num).values(author=auth,content=cont)
        conn.execute(updation)
        return redirect(url_for("blogs"))
        
    sel=blog.select().where(blog.c.id==num)
    exe=conn.execute(sel)
    result=exe.fetchone()
    return render_template("editpage.html",data=result)

if __name__=="__main__":
    app.run(debug=True)



    