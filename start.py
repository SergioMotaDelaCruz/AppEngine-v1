import logging

from flask import Flask, render_template, request, jsonify
from google.appengine.ext import ndb
from google.appengine.api import memcache, namespace_manager
#test

application = Flask(__name__)

class Version(ndb.Model):
   likes=ndb.FloatProperty()
   views=ndb.FloatProperty()


@application.route('/')
def home():
   namespace_manager.set_namespace('VER_1')
   v1=Version.get_by_id('v1')
   if not v1:
      v1=Version(likes=1,views=1,id='v1')
      v1_key=v1.put()
   #print '------'
   #print request.user_agent
   #print request.remote_addr
   #print request.headers
   #print '------'

   v1_last=Version.get_by_id('v1')
   v1_last.views+=1
   v1_last.put()
   return render_template('home.html')

@application.route('/sumav1', methods=['POST'])
def sumav1():
   namespace_manager.set_namespace('VER_1')
   v1_last=Version.get_by_id('v1')
   v1_last.likes+=1
   v1_last.put()
   return render_template('like-v1.html')

@application.route('/stats/v1', methods=['GET'])
def stats_v1():
   namespace_manager.set_namespace('VER_1')
   data={"version":namespace_manager.get_namespace(),"views":Version.get_by_id('v1').views,"likes":Version.get_by_id('v1').likes}
   return jsonify(data)

@application.errorhandler(500)
def server_error(e):
    logging.exception('Error during request. '+str(e))
    return 'An internal error occurred.', 500