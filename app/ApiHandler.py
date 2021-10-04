from flask_restful import Api, Resource, reqparse

class ApiHandler(Resource):
    def get(self): 
        return {
            'resultStatus': 'SUCCESS',
            'message': "Hello Api Handler"
        }

    def post(self):
        print(self)
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str)
        parser.add_argument('message', type=str)

        args = parser.parser_args()

        print(args)

        request_type = args['type']
        request_json = args['message']

        ret_status = request+type
        ret_msg = request_json
        
        if (ret_msg):
            message = "Your Mesage Requested: {}".format(ret_msg)
        else:
            message = "No Message"

        final_ret = {"status": "Success", "message": message}

        return final_ret 
