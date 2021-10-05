from flask import Flask, session, render_template, redirect, request, flash
from recipes_app import app
from recipes_app.controllers import recipes_controller, users_controller


if __name__ == '__main__':
    app.run(debug=True)