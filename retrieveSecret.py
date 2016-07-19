from keystoneclient.auth import identity
from keystoneclient import session
from barbicanclient import client

#We'll use Keystone API v3 for authentication
auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
			     username=u'admin',
			     user_domain_name=u'Default',
			     password=u'nomoresecret',
			     project_name=u'admin',
			     project_domain_name=u'Default')

#Next we'll create a keystone session using the auth plugin we just created
sess = session.Session(auth=auth)

#Now we use the session to create a Barbican client
barbican = client.Client(session=sess)

sec = barbican.secrets.list()
#print sec

for ref in sec:
	print ref.name
	print ref.created
	print ref.secret_ref
