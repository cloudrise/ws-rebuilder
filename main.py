import boto3, argparse, sys, time

# Creates AWS session.
# Returns session object with specified region and with/without AWS credentials.
def create_session(accesskey, secretkey, region):
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
def get_workspace_details(session):
    all_workspaces = []
    try:
        client = session.client('workspaces')
        response = client.describe_workspaces()
        while response:  
            all_workspaces += response['Workspaces']
            response = client.describe_workspaces(NextToken = response['NextToken']) if 'NextToken' in response else None # Pagination handling
    except Exception as e:
        print("Something wrong while getting workspaces details. ", e)
    
    return all_workspaces

# Rebuild given workspace
def rebuild_workspace(session, to_rebuild):
    client = session.client('workspaces')
    print("Rebuilding in progress: ", to_rebuild)
    try:
        response = client.rebuild_workspaces(
            rebuild_workspaceRequests=[
                {
                    'WorkspaceId' : to_rebuild
                }
            ]
        )
    except Exception as e:
        print("Something wrong while rebuilding workspace.", e)

# Start given workspace
def start_workspace(session, to_start):
    client = session.client('workspaces')
    print("Starting in progress: ", to_start)
    try:
        response = client.start_workspaces(
        start_workspaceRequests=[
            {
                'WorkspaceId' : to_start
            }
        ]
           )
    except Exception as e:
        print("Something wrong while starting WS. ", e)

# Check if all workspaces are in AVAILABLE state
def check_if_all_started(session):
    all_workspaces = get_workspace_details(session)
    for workspace in all_workspaces:
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

    session = create_session(args.accesskey, args.secretkey, args.region)

    all_workspaces = get_workspace_details(session)

    print("WorkSpaces must be started before rebuilding.")
    for workspace in all_workspaces:
        if workspace["State"] == "STOPPED":
            start_workspace(session, workspace["WorkspaceId"])

    while not check_if_all_started(session):
        print("Not all WorkSpaces are running. Next check in 30 seconds.")
        time.sleep(30)

    confirm = input("Are you sure to REBUILD all WorkSpaces? [YES]: ")

    if confirm == "YES":
        for workspace in all_workspaces:
            rebuild_workspace(session, workspace["WorkspaceId"])
    else:
        print("Rebuilding canceled.")

if __name__ == '__main__':
    main()
