from flask import Flask, render_template, request
import pickle
import numpy as np

# setup application
app = Flask (__name__)

def prediction(lst):
    filename = 'model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value

@app.route('/', methods=['POST', 'GET'])
def index():
    pred = 0
    if request.method == 'POST':
        ram = request.form['ram']
        weight = request.form['weight']
        hdd = request.form['hdd']
        ssd = request.form['ssd']
        company = request.form['company']
        typename = request.form['typename']
        opsys = request.form['opsys']
        resolution = request.form['resolution']
        inches = request.form['inches']
        cpu = request.form['cpu']
        gpu = request.form['gpu']
        touchscreen = request.form.getlist('touchscreen')
        ips = request.form.getlist('ips')

        feature_list = []
        feature_list.append(int(ram))
        feature_list.append(float(weight))
        feature_list.append(len(touchscreen))
        feature_list.append(len(ips))
        feature_list.append(int(hdd))
        feature_list.append(int(ssd))

        company_list = ['asus', 'acer', 'apple', 'dell', 'hp', 'lenovo', 'msi', 'other', 'toshiba']
        typename_list = ['2 in 1 convertible', 'gaming', 'notebook', 'netbook', 'ultrabook', 'workstation']
        opsys_list = ['linux', 'mac', 'windows', 'noos', 'other']
        resolution_list = ['1366x768', '1600x900', '1920x1080', '2560x1440', '3200x1800', '3840x2160', 'other']
        cpu_list = ['amd', 'intelcorei3', 'intelcorei5', 'intelcorei7', 'other']
        gpu_list = ['amd', 'intel', 'nvidia']
        inches_list = ['11.6', '12.5', '13.3', '14.0', '15.6', '17.3']  

        def traverse_list(lst, value):
            for item in lst:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)
        
        traverse_list(company_list, company)
        traverse_list(typename_list, typename)
        traverse_list(opsys_list, opsys)
        traverse_list(resolution_list, resolution)
        traverse_list(cpu_list, cpu)
        traverse_list(gpu_list, gpu)
        traverse_list(inches_list, inches)

        pred = prediction(feature_list)
        pred = np.round(pred[0])
        


    return render_template("index.html", pred = pred)

if __name__ == '__main__':
    app.run(debug=True)