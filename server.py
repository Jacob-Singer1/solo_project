from flask_app import app
from flask_app.controllers import user_controller, deck_controller





if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True) # app.run(debug=True) should be the very last statement!