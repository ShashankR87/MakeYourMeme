from flask import Flask, render_template, request, url_for
import requests
import urllib.request

resp = requests.get('https://api.imgflip.com/get_memes')
if resp.status_code != 200:
	print('Error')

resp = resp.json()
data = resp["data"]
print(resp)
cnt = 0
memes = dict()
username = "bobbyboibobby"
password = "bobbyboibobby"
for item in data["memes"]:
    if cnt == 8:
        break
    if item["box_count"] == 2:
        memes[item["id"]] = item["url"]
        cnt += 1


print(memes.values())
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        details = request.form
        selected_img = details["meme"]
        text0 = details["text0"]
        text1 = details["text1"]
        new_meme = {"template_id":selected_img,"username": username,"password":password,"text0":text0,"text1":text1}
        resp = requests.post('https://api.imgflip.com/caption_image',params=new_meme)
        if resp.json()['success'] != True:
            return resp.json()['error_message']
        else:
            gen_url = resp.json()['data']['url']
            return render_template('index.html',memeID=list(memes.keys()),memeU=list(memes.values()),res=gen_url)
    return render_template('index.html',memeID=list(memes.keys()),memeU=list(memes.values()),res='')




if __name__ == '__main__':
    app.run(debug=True)
    