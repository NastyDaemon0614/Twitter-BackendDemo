from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app=Flask(__name__)
client=MongoClient()
datab=client.tweetdb
tweets=datab.tweets

@app.route('/', methods=['GET','POST','PUT'])
def tweet():

    if request.method == 'POST':
        data=request.json
        tweetid = data.get('tweetid',0)
        username= data.get('username','Anonymous')
        content=data.get('content','NULL')
        likes=0

        result=tweets.insert_one({
            'username': username,
			'tweetid':tweetid,
            'content': content,
            'likes':likes
        })

        response={
            'message':'Tweet Posted',
            'obj_id': str(result.inserted_id)
        }

        return jsonify(response),201
    
    elif request.method =='GET':

        result = tweets.find({},{'_id':0})

        response={
            'data':list(result)
        }
        return jsonify(response)

    elif request.method =='PUT':
        newvalue=request.json.get('updatelike',1)
        tweetid=request.json.get('tweetid',0)

        for r in tweets:
            if tweetid==r['tweetid']:
                r['likes']=newvalue

        response={
            'message':'Tweet updated'
        }

        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)