from flask import  jsonify
from backend.extentions import get_db
from auth.jwt_utils import get_current_user_id

def register_user_profile(app):

    @app.route('/users')
    def users_list():
        if get_current_user_id is None:
            return jsonify ({"message": "unaurthorised"})

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id , name , email FROM users ORDER BY name")
        rows = cur.fetchall()



        return jsonify([
                    {
                        "id": str(r["id"]),
                        "name": r["name"],
                        "email": r["email"],
                        
                    }
                    for r in rows
                ]) , 200
    
