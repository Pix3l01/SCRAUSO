from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['PUT'])
def answer():
    token = request.headers.get('X-Team-Token', '')
    print(token)
    if token != 'token':
        return jsonify("Token sbagliato")

    data = request.get_json(force=True)
    print(data)

    responses = []
    for flag in data:
        msg = 'Flag accepted! Earned 5 flag points!'
        if flag[-2] == "f":
            msg = 'Flag is too old'
        if flag[-2] == "4":
            msg = 'Flag is invalid or too old.'
        if flag[-2] == "b":
            msg = 'Flag already stolen'
        responses.append(
            {
                'msg': f'[{flag}] {msg}',
                'flag': flag,
            }
        )

    return jsonify(responses)
app.run(host='0.0.0.0', port=31337)
