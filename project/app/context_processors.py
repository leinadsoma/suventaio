# -*- encoding: utf-8 -*-
from config.settings import APPTITLE, APPTEXT
import datetime

def globalvar(request):
	apptitle = APPTITLE
	apptext = APPTEXT
	now = datetime.datetime.now()
	return{
			'apptitle' : apptitle,
			'apptext' : apptext,
			'now' : now,
		}