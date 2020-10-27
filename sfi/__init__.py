from flask import Flask, render_template
from sfi import email_sender
from sfi import forms
import os


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SMTP_SERVER") or "very_very_secret_key_to_be_changed_in_production"

    @app.route("/test")
    def test():
        return "<h3> ### mrcn ### heroku ### </h3>"

    @app.route("/send_mail", methods=["GET", "POST"])
    def send_mail():
        form = forms.MailForm()
        if form.validate_on_submit():
            es = email_sender.MailSender()
            es.send_mail(subject=form.subject.data, message=form.message.data)
            return render_template("index.html", form=forms.MailForm())
        return render_template("index.html", form=form)

    return app
