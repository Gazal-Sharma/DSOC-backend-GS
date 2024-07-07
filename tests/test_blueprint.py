# from flask import Flask
# from app.blueprints.post_prod.post_prod import post_pd

# main = Flask(__name__)
# main.register_blueprint(post_pd)
# with main.test_client() as client:
#     # Make a GET request to '/example/test'
#     response = client.get('post_pd/create_product')
    
#     # Assert that the response is successful (HTTP status code 200)
#     assert response.status_code == 200
    
#     # Print the response data
#     print(response.data.decode('utf-8'))