from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/hi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    surname = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return self.name

@app.route('/', methods=['post', 'get'])
def main():
    if request.method == 'POST':
        try:
            name, surname = request.form.get('name').split(' ')
    
            if Name.query.filter_by(name=name).first() == None:
                db.session.add(Name(name=name, surname=surname))
                text = 'Привіт, {} {}'.format(name, surname)
            else:
                text = 'Вже бачилися, {}'.format(name)
            db.session.commit()
        except:
            text = 'Вибачте, ви не коректно ввели дані'
        form = False
    else:
        form = True
        text = ''
    context = {
        'form':form,
        'text':text
    }
    return render_template('main_page.html', **context)

@app.route('/list')
def list_of_names():
    page = request.args.get('page', 1, type=int)
    names = Name.query.paginate(page=page, per_page=7)
    return render_template('list_of_names.html', names=names)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')