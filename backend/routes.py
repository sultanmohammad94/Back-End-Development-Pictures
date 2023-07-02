from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200
    return jsonify({"message": "Data not found"})

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    id = int(id)
    for item in data:
        if int(item.get("id")) == id:
            return jsonify(item), 200
    return jsonify({"message": "Data not found"}), 404




######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():   
    new_pic = request.get_json()
    for pic in data:
        same_ec = pic["event_country"] == new_pic['event_country']
        same_es = pic["event_state"] == new_pic['event_state']
        same_ect = pic["event_city"] == new_pic['event_city']
        same_dt = pic["event_date"] == new_pic['event_date']
        conds = [same_ec, same_es, same_ect, same_dt]
        if all(conds):
           
            return jsonify({"Message": f"picture with id {pic['id']} already present" }), 302
    data.append(new_pic)
    return jsonify(new_pic), 201
            


        

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    for pic in data:
        if pic['id'] == id:
            pic['pic_url'] = request.json['pic_url']
            pic['event_country'] = request.json['event_country']
            pic['event_city'] = request.json['event_city']
            pic['event_state'] = request.json['event_state']
            pic['event_date'] = request.json['event_date']
            return jsonify(pic), 200
    else:
        return jsonify({"message": "picture not found"}), 404
######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for pic in data:
        if pic["id"] == id:
            data.remove(pic)
            return jsonify({"message": ""}), 204
    return jsonify({"message": "picture not found"}), 404
