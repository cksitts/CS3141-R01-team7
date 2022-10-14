from app import l_app

@l_app.route('/')
@l_app.route('/index')
def index():
    return 'default.';
