from flask import Flask
from flask import request, json
import process
import constants

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    data = json.loads(request.data) 
    
    process.firstCopy()
    process.getCodeFromGitHub()  # git clone
    #if branch not main do only test
        #process.buildtest
        #process.deploytest
        #ans =test.runtest
        #if ans ok send mail

    #if branch main test and deploy
        #process.buildtest
        #process.deploytest
        #ans =test.runtest
        #if ans ok send mail
        #if test ok deploy production
    process.dockerBuild_Billing() 
    
    process.dockerBuild_Weight()
    process.productionDeploy_Weight() 
    process.productionDeploy_Billing()

    # !!!main will call functions from process.py! this part will be depreciated.
    # Call bash script to process for git trigger
    # subprocess.check_call("./process.sh '%s'" % data['ref'], shell=True)
    # commits = json.dumps(data['commits'])

    return data['ref']


# def get_code():
#     print('getcode')


# def build():
#     print('build')


# def test():
#     print('test')


# def deploy():
#     print('deploy')


# def send_mail():
#     list_admin = ['admin@mydomain.com']
#     if not app.debug:
#         import logging
#         from logging.handlers import SMTPHandler
#         mail_handler = SMTPHandler(mailhost=('smtpout.secureserver.net', 25),
#                                    fromaddr='admin@mydomain.com',
#                                    toaddrs=list_admin, subject='YourApplication Failed',
#                                    credentials=('admin@mydomain.com', 'mypassword'))
#         mail_handler.setLevel(logging.ERROR)
#         app.logger.addHandler(mail_handler)

        
if __name__ == '__main__':
    app.run(host=constants.HOST, port=constants.PORT, debug=constants.TEST)
    # debug=True only in test. should be off in prod!