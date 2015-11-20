from flask import render_template, Flask , url_for
import urllib
from gsheets_wrap import GsDownloader
import json
import templates

app = Flask(__name__)

@app.route('/')
def main():
    # import pdb; pdb.set_trace()
    routes_list = sorted(fetch_route_list())
    
    context = {'Routes': routes_list }  
    return render_template('main.html', **context)
#    return str(app.url_map)

@app.route('/menu')
def menu():
    routes_list = sorted(fetch_route_list())

    context = {
        'COPY': GsDownloader(sheetfilename='Menus').sheetdata(),
        'Routes': routes_list
    }

    main()

    return render_template('menu.html', **context)

@app.route('/testData', defaults={'sheet': 'fake'})
@app.route('/testData/<sheet>')
def testheets(sheet):

    routes_list = sorted(fetch_route_list())

    context = {
        'COPY': GsDownloader(sheetfilename=sheet).sheetdata()
        ,'Routes': routes_list
    }

    return render_template('test_features.html', **context)
    #return json.dumps(context)


@app.route('/testFoundation')
def testfeatures():
    routes_list = sorted(fetch_route_list())

    context = {
        'COPY': GsDownloader(sheetfilename='Menus').sheetdata(),
        'Routes': routes_list
    }

    return render_template('foundation_features.html', **context)



def fetch_route_list():
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        #line = urllib.unquote("{0} : {1}  {2}".format(rule.endpoint, methods, url))
        line = {'url': urllib.unquote("{}".format(url)), 'methods':methods, 'rule': rule.endpoint }
        output.append(line)
    return output


if __name__ == "__main__":
    app.run(debug=True)