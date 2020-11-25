from logging import debug
from os import terminal_size
from flask.globals import current_app

from socketmgr import socketio, app

import logging #Why no work ಥ_ಥ
logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

if __name__ == "__main__":
    print('\n\n\nRunning\n-----------------')
    socketio.run(app, host='0.0.0.0', port=80, use_reloader=False, log_output=False, debug=True)