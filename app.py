from flask import Flask, render_template, request, url_for, session, redirect, send_file, jsonify
import requests
import urllib.request
import webbrowser
from flask_restful import Resource, Api

resp = requests.get('https://api.imgflip.com/get_memes')
if resp.status_code != 200:
	print('Error')

resp = resp.json()
data = resp["data"]
cnt = 0
memes = dict()
username = "bobbyboibobby"
password = "bobbyboibobby"
for item in data["memes"]:
    if cnt == 8:
        break
    if item["box_count"] == 2:
        memes[item["id"]] = [item["url"], item["name"]]
        cnt += 1


print(memes.values())
app = Flask(__name__)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

api = Api(app)

class MemeClass(Resource):
    def get(self, name):
        resp = requests.get('https://api.imgflip.com/get_memes')
        if resp.status_code != 200:
            print('Error')

        resp = resp.json()
        data = resp["data"]
        item = [d for d in data["memes"] if d["name"] == name]
        if len(item) == 0:
            item.append(dict())
            item[0]["status"] = 'Error'
            item[0]["desc"] = "No such meme found."
            return jsonify(item)
        else:
            item[0]["status"] = 'OK'
            memename = item[0]["name"]
            memew = item[0]["width"]
            memeh = item[0]["height"]
            memeb = item[0]["box_count"]
            memeu = item[0]["url"]
            return jsonify(item)
            
api.add_resource(MemeClass, '/meme/<name>')

@app.route('/memeWeb/<name>', methods=['GET'])
def memeWeb(name):
    resp = requests.get('https://api.imgflip.com/get_memes')
    if resp.status_code != 200:
        print('Error')

    resp = resp.json()
    data = resp["data"]
    item = [d for d in data["memes"] if d["name"] == name]
    if len(item) == 0:
        return render_template('meme.html',name = '', w = '', h = '', b = '', u = '')
    else:
        memename = item[0]["name"]
        memew = item[0]["width"]
        memeh = item[0]["height"]
        memeb = item[0]["box_count"]
        memeu = item[0]["url"]
        return render_template('meme.html',name = memename, w = memew, h = memeh, b = memeb, u = memeu)
    



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        details = request.form
        selected_img = details.getlist("meme")
        print(selected_img)
        session["selected_img"] = selected_img
        #text0 = details["text0"]
        #text1 = details["text1"]
        return redirect(url_for('checkout'))


        new_meme = {"template_id":selected_img,"username": username,"password":password,"text0":text0,"text1":text1}
        resp = requests.post('https://api.imgflip.com/caption_image',params=new_meme)
        if resp.json()['success'] != True:
            return resp.json()['error_message']
        else:
            gen_url = resp.json()['data']['url']
            return render_template('index.html',memeID=list(memes.keys()),memeU=list(memes.values()),res=gen_url)
    return render_template('index.html',memeID=list(memes.keys()),memeU=list(memes.values()),res='')



@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    selected_img = session["selected_img"]
    selected_URL = [memes[k] for k in selected_img]
    if request.method == 'POST':
        for memeid in selected_img:
            if str(memeid)+" rem" in request.form:
                ind = selected_img.index(memeid)
                selected_img.remove(memeid)
                selected_URL.remove(selected_URL[ind])
                session["selected_img"] = selected_img
                return redirect(url_for('checkout'))

        texts=[]
        details = request.form
        for i in range(len(selected_img)):

            t0 = details[str(selected_img[i])+" 0"]
            t1 = details[str(selected_img[i])+" 1"]
            texts.append([selected_img[i],t0,t1])
        session["selected_texts"] = texts
        return redirect(url_for('preview'))

    
    return render_template('checkout.html',numOfMemes = len(selected_img),memeID=selected_img,memeU=selected_URL)


@app.route('/preview', methods=['GET', 'POST'])
def preview():
    selected_img = session["selected_img"]
    selected_URL = [memes[k] for k in selected_img]
    selected_texts = session["selected_texts"]
    print(selected_texts)
    gen_urls=[]
    for i in range(len(selected_img)):
        new_meme = {"template_id":selected_img[i],"username": username,"password":password,"text0":selected_texts[i][1],"text1":selected_texts[i][2]}
        resp = requests.post('https://api.imgflip.com/caption_image',params=new_meme)
        if resp.json()['success'] != True:
            return resp.json()['error_message']
        else:
            gen_urls.append(resp.json()['data']['url'])
    


    if request.method == 'POST':
        for memeid in selected_img:
            if str(memeid)+" rem" in request.form:
                ind = selected_img.index(memeid)
                selected_img.remove(memeid)
                gen_urls.remove(gen_urls[ind])
                session["selected_img"] = selected_img
                return redirect(url_for('preview'))
            if str(memeid)+" edit" in request.form:
                details = request.form
                ind = selected_img.index(memeid)
                t0 = details[str(memeid)+" 0"]
                t1 = details[str(memeid)+" 1"]
                selected_texts[ind] = [memeid,t0,t1]
                session["selected_texts"] = selected_texts
                return redirect(url_for('preview'))
            
        
            


        texts=[]
        details = request.form
        for i in range(len(selected_img)):

            t0 = details[str(selected_img[i])+" 0"]
            t1 = details[str(selected_img[i])+" 1"]
            texts.append([selected_img[i],t0,t1])
        session["selected_texts"] = texts
        return redirect(url_for('preview'))
    return render_template('preview.html',numOfMemes = len(selected_img),memeID=selected_img,memeU=gen_urls)
    

if __name__ == '__main__':
    app.run(debug=True)
    