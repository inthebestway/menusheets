from flask import render_template, Flask 

from gsheets_wrap import GsDownloader
import json
import templates

app = Flask(__name__)



@app.route('/menu')
def menu():
    context = {
        'COPY': GsDownloader(sheetfilename='Menus').sheetdata()
    }

    return render_template('menu.html', **context)


@app.route('/testData')
def index():
    context = {
        'COPY': GsDownloader(sheetfilename='fake').sheetdata()
    	#'COPY' : {'a':1 }
    }

    return render_template('test_features.html', **context)
    #return json.dumps(context)


@app.route('/testFoundation')
def testfeatures():
    context = {
        'COPY': GsDownloader(sheetfilename='Menus').sheetdata()
    }

    return render_template('foundation_features.html', **context)


if __name__ == "__main__":
    app.run(debug=True)