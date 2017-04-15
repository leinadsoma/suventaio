from django import template
from django.template.loader import get_template
from django.template import Context, Template
register = template.Library()
from django.shortcuts import render
from project.app.models import *
import re

