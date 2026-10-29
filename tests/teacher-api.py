import sys,json,urllib.request,urllib.error,getpass
url='https://nltqzuhubqhwtfxwuupr.supabase.co/functions/v1/tangram-teacher'
key='sb_publishable_lnFCcbPSjbJg_z6QG-KZUw__n6rnwll'
password=getpass.getpass('Teacher password: ')
def req(body,token=None):
 headers={'Content-Type':'application/json','apikey':key,'Origin':'https://wongngaiyam3-rgb.github.io'}
 if token:headers['x-teacher-session']=token
 try:
  r=urllib.request.urlopen(urllib.request.Request(url,data=json.dumps(body).encode(),headers=headers),timeout=25)
  return r.status,json.loads(r.read())
 except urllib.error.HTTPError as e:return e.code,json.loads(e.read())
assert req({'action':'report'})[0]==401
assert req({'action':'report'},'forged-token')[0]==401
assert req({'action':'login','password':'incorrect-test-password'})[0]==401
status,data=req({'action':'login','password':password});assert status==200,(status,data)
token=data['session'];status,data=req({'action':'report'},token);assert status==200,(status,data)
assert all('owner_token' not in r and 'board' not in r for r in data['records'])
status,data=req({'action':'report','class_name':'4A','student_number':1},token);assert status==200,(status,data)
assert all(r['class_name']=='4A' and r['student_number']==1 for r in data['records'])
assert req({'action':'report','class_name':'4Z'},token)[0]==400
print('PASS: live Edge password login, all-class report, class/number filtering and no private device tokens exposed.')
