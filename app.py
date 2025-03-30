from flask import Flask,jsonify
from config import mongo
from routes.user_routes import user_routes
from routes.water_intake_routes import water_bp
from routes.health_log_routes import health_bp
from routes.steps_routes import steps_bp
from routes.heart_rate_routes import heart_rate_bp
from routes.sleep_routes import sleep_bp
from routes.stress_routes import stress_bp
from routes.day_rating_route import day_rating_bp

app = Flask(__name__) 
app.register_blueprint(user_routes)
app.register_blueprint(water_bp)
app.register_blueprint(health_bp)
app.register_blueprint(steps_bp)
app.register_blueprint(heart_rate_bp)
app.register_blueprint(sleep_bp)
app.register_blueprint(stress_bp)
app.register_blueprint(day_rating_bp)

# Pass the required route to the decorator. 
@app.route('/',methods=['GET']) 
def home(): 
	return jsonify({"message":"Vitalflow API is running..."})
	

if __name__ == "__main__": 
	app.run(debug=True) 
