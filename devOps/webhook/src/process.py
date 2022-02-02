import os, subprocess

# from git import Repo
from mailingService.mail_Service import sendErrorToLog, mailNotification


import constants

# TODO: fix error
# Error: While importing 'main', an ImportError was raised.
def firstCopy():
    if  not os.path.isdir('GanShmuel'):
        try:
            subprocess.run("git clone https://github.com/develeapDorZ/GanShmuel", shell=True, check=True)
        except:
            sendErrorToLog('repo_log.txt', 'failed', 'repo creation')
            mailNotification('updateRepo', 'devops', False)
            terminateContainer()
            return True, False
        else:
            mailNotification('updateRepo', 'devops', True)
            sendErrorToLog('repo_log.txt', 'success', 'repo creation')
            return True, True
    else:
        return False, False


def getCodeFromGitHub():
    # git clone git@github.com:develeapDorZ/GanShmuel.git
    try:
        #Repo.pull(os.path.join(constants.gitHubURL, constants.deployDirectory))
        # pull -f --all - update the whole repo
        subprocess.run("git -C GanShmuel pull -f --all", shell=True, check=True)#noticed this can cause conflicts problematic???  

    except:
        sendErrorToLog('repo_log.txt', 'failed', 'repo update')
        mailNotification('updateRepo', 'devops', False)
        terminateContainer()
        return False
    else:
        mailNotification('updateRepo', 'devops', True)
        sendErrorToLog('repo_log.txt', 'success', 'repo update')
        return True


def dockerBuild(branchName):
    try:
        subprocess.run("docker-compose -f ./GanShmuel/{branchName}/docker-compose.yml build", shell=True, check=True)

    except:
        sendErrorToLog('{branchName}_team_log.txt', 'failed', 'build')
        mailNotification('build', branchName, False)
        terminateContainer()
        return False
    else:
        mailNotification('build', branchName, True)
        sendErrorToLog('{branchName}_team_log.txt', 'success', 'build')
        return True


def dockerDeploy(branchName, env):
    try:
        subprocess.run("docker-compose -f ./GanShmuel/{branchName}/docker-compose.yml up -d", shell=True, check=True)

    except:
        sendErrorToLog('{branchName}_team_log.txt', 'failed', 'deploy')
        mailNotification('build', branchName, False)
        terminateContainer()
        return False
    else:
        mailNotification('build', branchName, True)
        sendErrorToLog('{branchName}_team_log.txt', 'success', 'deploy')
        return True


def testingDeploy(branchName):
    # TODO: run docker-compose for testing
    # docker-compose up -d >> /app/test.log
    try:
        #subprocess.run("docker-compose -f ./GanShmuel/billing/docker-compose.yml up -d", shell=True, check=True)
        # -- Need to hookup with the testing
        print("i am here because I have no code yet")

    except:
        sendErrorToLog('{branchName}_team_log.txt', 'failed', 'test')
        mailNotification('build', branchName, False)
        terminateContainer()
        return False
    else:
        mailNotification('build', branchName, True)
        sendErrorToLog('{branchName}_team_log.txt', 'success', 'test')
        return True


def terminateContainer():
    # ---- WHat are the containers names defined by the teams
    if subprocess.run('docker ps | grep "billing_test"') == "billing_test":
        subprocess.run("docker-compose billing_test down")
    if subprocess.run('docker ps | grep "weight_test"') == "weight_test":
        subprocess.run("docker-compose weight_test down")
    

# def dockerBuild_Billing():
#     try:
#         subprocess.run("docker-compose -f ./GanShmuel/billing/docker-compose.yml build", shell=True, check=True)

#     except:
#         sendErrorToLog('billing_team_log.txt', 'failed', 'build')
#         mailNotification('build', 'billing', False)
#     else:
#         mailNotification('build', 'billing', True)
#         sendErrorToLog('billing_team_log.txt', 'success', 'build')

# def deploy_Weight(env):
#     try:
#         subprocess.run("docker-compose -f ./GanShmuel/weight/docker-compose.yml up -d", shell=True, check=True)

#     except:
#         sendErrorToLog('weight_team_log.txt', 'failed', 'deploy')
#         mailNotification('deploy', 'weight', False)
#     else:
#         mailNotification('deploy', 'weight', True)
#         sendErrorToLog('weight_team_log.txt', 'success', 'deploy')


# def testingDeploy_Billing():
#     # TODO: run docker-compose for testing
#     # docker-compose up -d >> /app/test.log
#     try:
#         subprocess.run("docker-compose -f ./GanShmuel/billing/docker-compose.yml up -d", shell=True, check=True)

#     except:
#         sendErrorToLog('billing_team_log.txt', 'failed', 'deploy')
#         mailNotification('deploy', 'billing', False)
#     else:
#         mailNotification('deploy', 'billing', True)
#         sendErrorToLog('billing_team_log.txt', 'success', 'deploy')


# def testingDeploy_Weight():
#     try:
#         subprocess.run("docker-compose -f ./GanShmuel/weight/docker-compose.yml up -d", shell=True, check=True)

#     except:
#         sendErrorToLog('weight_team_log.txt', 'failed', 'deploy')
#         mailNotification('deploy', 'weight', False)
#     else:
#         mailNotification('deploy', 'weight', True)
#         sendErrorToLog('weight_team_log.txt', 'success', 'deploy')
