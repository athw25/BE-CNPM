def register_controllers(app):
    from api.controllers.user_controller import users_bp
    from api.controllers.intern_controller import interns_bp
    from api.controllers.recruitment_controller import bp as recruitment_bp
    from api.controllers.application_controller import bp as application_bp
    from api.controllers.training_controller import training_bp
    from api.controllers.project_controller import project_bp
    from api.controllers.assignment_controller import assignment_bp
    from api.controllers.evaluation_controller import evaluations_bp

    app.register_blueprint(users_bp,        url_prefix="/api")
    app.register_blueprint(interns_bp,      url_prefix="/api")
    app.register_blueprint(recruitment_bp)   # đã có /api trong file
    app.register_blueprint(application_bp)   # đã có /api trong file
    app.register_blueprint(training_bp)      # đã có /api trong file
    app.register_blueprint(project_bp)       # nếu tách project riêng
    app.register_blueprint(assignment_bp)    # đã có /api trong file
    app.register_blueprint(evaluations_bp,  url_prefix="/api")
