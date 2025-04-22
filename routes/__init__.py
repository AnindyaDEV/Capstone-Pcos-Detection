from .pages import page_routes
from .diagnosis import diagnosis_api
from .ultrasound import ultrasound_api
from .menstrual import menstrual_routes
from .fitness import fitness_routes  # ✅ NEW
from routes.nutrition import nutrition_bp
from routes.chatbot import chatbot_bp
from routes.gynecologist import gynecologist_bp
from routes.pharmacy import pharmacy_bp




def init_routes(app):
    app.register_blueprint(page_routes)
    app.register_blueprint(diagnosis_api)
    app.register_blueprint(ultrasound_api)
    app.register_blueprint(menstrual_routes)
    app.register_blueprint(fitness_routes)  # ✅ Register fitness route
    app.register_blueprint(nutrition_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(gynecologist_bp)
    app.register_blueprint(pharmacy_bp)
