from flask import Flask,jsonify
from config import mongo
from routes.user_routes import user_routes
from routes.water_intake_routes import water_bp
from routes.health_log_routes import health_bp
from routes.steps_routers import steps_bp

app = Flask(__name__) 
app.register_blueprint(user_routes)
app.register_blueprint(water_bp)
app.register_blueprint(health_bp)
app.register_blueprint(steps_bp)

# Pass the required route to the decorator. 
@app.route('/',methods=['GET']) 
def home(): 
	return jsonify({"message":"Vitalflow API is running..."})
	

if __name__ == "__main__": 
	app.run(debug=True) 
