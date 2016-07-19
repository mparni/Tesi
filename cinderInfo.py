from keystoneclient.auth import identity
from keystoneclient import session
from cinderclient import client

#We'll use Keystone API v3 for authentication
auth = identity.v3.Password(auth_url=u'http://localhost:5000/v3',
			     username=u'admin',
			     user_domain_name=u'Default',
			     password=u'nomoresecret',
			     project_name=u'admin',
			     project_domain_name=u'Default')

#Next we'll create a keystone session using the auth plugin we just created
sess = session.Session(auth=auth)

#Now we use the session to create a Cidner client
cinder = client.Client('3',session=sess)

sec = cinder.volumes.list()
#print sec

count = 0
for ref in sec:
	print ("\n")
	print ref.id
	print ref.name
	print ref.status
	print ref.volume_type
	print ("\n")
	if (ref.volume_type == 'LUKS'):
#		print ("------------------------\n %s e' LUKS"  % ref.id)
#		test = cinder.volumes.get(ref.id)
#		print test.id
#		print test.size
#		print test.encrypted
#		print test.created_at
#		print test.status
		count += 1

print (count)
