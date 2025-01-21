from flask import Flask, request, render_template, jsonify, Response
from flask_cors import CORS
from pymongo import MongoClient
from gridfs import GridFS
from bson.objectid import ObjectId
from io import BytesIO
# Flask app setup
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
CORS(app)



# MongoDB and gridfs setup
client = MongoClient('mongodb+srv://nightanon038:dah9NfhKw71cA9ix@test-cluster.l9zqd.mongodb.net/?retryWrites=true&w=majority&appName=test-cluster')  # Replace with your MongoDB URI
serverSelectionTimeoutMS=50000,
db = client['travel_platform']  # Database name
collection = db['posts']
fs = GridFS(db)  # GridFS for storing images

# Routes
@app.route('/')
def home():
    return render_template('forum.html')  # Render your HTML template


@app.route('/posts', methods=['GET'])
def get_all_posts():
    try:
        posts = list(collection.find({}))
        for post in posts:
            # Convert ObjectId to string for JSON
            post["_id"] = str(post["_id"])
            if post.get("image_id"):
                post["image_url"] = f"http://localhost:5000/file/{
                    post['image_id']}"
            if post.get("video_id"):
                post["video_url"] = f"http://localhost:5000/file/{
                    post['video_id']}"
        return jsonify(posts), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/add_post', methods=['POST'])
def add_post():
    try:
        # Get form data
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.get('tags', "").split(",")  # Split tags

        # Handle file uploads
        image_file = request.files.get('images')
        video_file = request.files.get('videos')

        image_id = None
        video_id = None

        if image_file:
            image_id = fs.put(image_file, filename=image_file.filename,
                              content_type=image_file.content_type)
        if video_file:
            video_id = fs.put(video_file, filename=video_file.filename,
                              content_type=video_file.content_type)

        # Insert post into MongoDB
        post = {
            "title": title,
            "content": content,
            "tags": tags,
            "image_id": str(image_id) if image_id else None,
            "video_id": str(video_id) if video_id else None
        }
        collection.insert_one(post)

        return jsonify({"message": "Post added successfully!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/file/<file_id>', methods=['GET'])
def get_file(file_id):
    try:
        # Retrieve file from GridFS
        file = fs.get(ObjectId(file_id))
        response = app.response_class(
            file.read(), content_type=file.content_type)
        response.headers["Content-Disposition"] = f"inline; filename={
            file.filename}"
        return response
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 404



if __name__ == '__main__':
    app.run(debug=True)




