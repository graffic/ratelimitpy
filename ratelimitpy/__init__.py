"""
Flask application with /hotels endpoint that demonstrates a rate limit
behaviour using a token bucket.
"""
import os
from flask import Flask, request, abort, jsonify
from ratelimitpy.db import HotelsRepository
from ratelimitpy.json_serialization import AppJSONEncoder
from ratelimitpy.api_key import set_api_key, require_api_key
from ratelimitpy.ratelimit import limit

app = Flask(__name__)
app.json_encoder = AppJSONEncoder
app.before_request(set_api_key)
app.config.update(dict(RATE_LIMITS={}))
app.config.from_pyfile(os.path.join(os.getcwd(), 'config.py'))

hotels_repository = HotelsRepository('hoteldb.csv')


@app.route('/hotels', methods=['GET'])
@require_api_key
@limit(requests=1, per_seconds=10, ban=5 * 60)
def hotels_endpoint():
    """List hotels by city name"""
    city = request.args.get("city")
    if city is None:
        abort(400)
    asc = request.args.get("asc", "true") == "true"
    return jsonify(result=hotels_repository.get_by_city(city, asc))


