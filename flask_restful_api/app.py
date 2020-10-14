from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('json_data', type=dict)


@app.after_request  # blueprint can also be app~~
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    response.headers.add(
        'Access-Control-Allow-Headers',
        "Origin, X-Requested-With, Content-Type, Accept, x-auth")
    response.headers.add('Access-Control-Allow-Methods',
                'GET, POST, OPTIONS, PUT, PATCH, DELETE')
    return response


def face_seriliser(face):
    # modifiy data for front-end use
    return {
        'distance': int(face['distance'] * 10),
        'x_cord': int(face['x_cord'] * 100),
        'timestamp': face['timestamp']
    }


def faces_seriliser(faces):
    faces_list = []
    for face in faces:
        faces_list.append(
            face_seriliser(face)
        )
    return faces_list


class CurrentlySeen(Resource):

    faces = {'seen_faces': []}

    def get(self):
        print(self.faces)
        return self.faces

    def put(self):
        args = parser.parse_args()
        print(args)
        json_data = args['json_data']
        print(json_data)
        self.faces['seen_faces'] = faces_seriliser(
            json_data['seen_faces']
        )
        print(self.faces)
        return self.faces


api.add_resource(CurrentlySeen, '/current_faces')

if __name__ == '__main__':
    app.run(debug=True)
