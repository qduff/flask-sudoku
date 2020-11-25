from socketmgr import socketio, app


if __name__ == "__main__":
    print('\n\n\nRunning\n'+'-'*30)
    socketio.run(app, host='0.0.0.0', port=80, use_reloader=False, log_output=False, debug=True)