import boto3, argparse, sys, time

# Creates AWS session.
# Returns session object with specified region and with/without AWS credentials.
def CreateSession(accesskey, secretkey, region):
    try:
        if not accesskey or not secretkey:
            return boto3.Session(
                region_name=region
            )
        else:
            return boto3.Session(
                aws_access_key_id=accesskey,
                aws_secret_access_key=secretkey,
                region_name=region)
    except Exception as e:
        print("Something wrong while creating AWS session. ", e)
        sys.exit()

# Returns list of WorkSpaces details
def GetWorkSpacesDetails(session):
    AllWorkSpaces = []
    try:
        client = session.client('workspaces')
        Response = client.describe_workspaces()
        while Response:  
            AllWorkSpaces += Response['Workspaces']
            Response = client.describe_workspaces(NextToken = Response['NextToken']) if 'NextToken' in Response else None # Pagination handling
    except Exception as e:
        print("Something wrong while getting workspaces details. ", e)
    
    return AllWorkSpaces

# Rebuild given workspace
def RebuildWorkSpace(session, toRebuild):
    client = session.client('workspaces')
    print("Rebuilding in progress: ", toRebuild)
    try:
        resp = client.rebuild_workspaces(
            RebuildWorkspaceRequests=[
                {
                    'WorkspaceId' : toRebuild
                }
            ]
        )
    except Exception as e:
        print("Something wrong while rebuilding workspace.", e)

# Start given workspace
def StartWorkSpace(session, toStart):
    client = session.client('workspaces')
    print("Starting in progress: ", toStart)
    try:
        response = client.start_workspaces(
        StartWorkspaceRequests=[
            {
                'WorkspaceId' : toStart
            }
        ]
           )
    except Exception as e:
        print("Something wrong while starting WS. ", e)

# Check if all workspaces are in AVAILABLE state
def CheckIfAllStarted(session):
    AllWorkSpaces = GetWorkSpacesDetails(session)
    for workspace in AllWorkSpaces:
        if workspace["State"] != "AVAILABLE":
            return False
    return True

def main():

    # Input args
    parser = argparse.ArgumentParser()
    parser.add_argument("region", help="Region where WorkSpaces are e.g eu-west-1.")
    parser.add_argument("--accesskey", help="Amazon Access Key ID. If not specified, IAM role will be used instead.")
    parser.add_argument("--secretkey", help="Amazon Secret Access Key. If not specified, IAM role will be used instead.")
    args = parser.parse_args()

    session = CreateSession(args.accesskey, args.secretkey, args.region)

    WorkSpaces = GetWorkSpacesDetails(session)

    print("WorkSpaces must be started before rebuilding.")
    for workspace in WorkSpaces:
        if workspace["State"] == "STOPPED":
            StartWorkSpace(session, workspace["WorkspaceId"])

    while not CheckIfAllStarted(session):
        print("Not all WorkSpaces are running. Next check in 30 seconds.")
        time.sleep(30)

    confirm = input("Are you sure to REBUILD all WorkSpaces? [YES]: ")

    if confirm == "YES":
        for workspace in WorkSpaces:
            RebuildWorkSpace(session, workspace["WorkspaceId"])
    else:
        print("Rebuilding canceled.")

if __name__ == '__main__':
    main()
