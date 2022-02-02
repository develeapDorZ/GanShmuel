from flask import Flask, request, json, render_template
import process
from constants import *

app = Flask(__name__)


@app.route('/',methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/monitoring', methods=['GET'])
def get_message():
    # process.testingDeploy_Billing()
    return {"billing":"Ok","weight":"err"}

@app.route("/webhook", methods=['POST'])
def webhook():
    data = json.loads(request.data) 
    
    # fetch branch name form data['ref']
    branchName = data['ref'].split("/")[-1]

    success, firstCopy = process.firstCopy()
    # if not success: return False

    if not firstCopy:
        process.getCodeFromGitHub(branchName)  # git clone
        # if not success: return False
    
    if branchName == 'biling': 
        branchName = 'billing' # location == branch (branch name fix)

    if branchName == "billing" or branchName == "weight" or branchName == "DevOps":

        process.dockerBuild(branchName)
        # if not success: return False

        process.dockerDeploy(branchName,'test')
        # if not success: return False

        # process.testingDeploy(branchName)
        # if not success: return False

    elif branchName == "main":

        # build, deploy and test weight
        process.dockerBuild("weight")
        # if not success: return False

        #process.dockerDeploy("weight",'test')
        # if not success: return False

        # process.testingDeploy("weight")
        # if not success: return False

        # build, deploy and test billing
        process.dockerBuild("billing")
        # if not success: return False

        # process.dockerDeploy("billing",'test')
        # if not success: return False

        # process.testingDeploy("billing")
        # if not success: return False


        # deploy to production
        process.dockerDeploy("weight",'production')
        # if not success: return False
        
        process.dockerDeploy("billing",'production')
        # if not success: return False

    return data['ref']

       
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # debug=True only in test. should be off in prod!
