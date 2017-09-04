from collections import namedtuple

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    
def parse(string):
	#[u'CSE', u'EEE', u'ECE'] to CSE, EEE, ECE
	print string 
	string = string.strip('[')
	string = string.strip(']')
	string = string.replace('u','')
	string = string.replace("'",'')
	print string
	return string
# with connection.cursor() as c:
 #    	c.execute('select * from user_profile where username = %s',[str(request.user.username)])
 #    	row = cursor.fetchone()