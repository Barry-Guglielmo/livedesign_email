def body(text):
    EMAIL_BODY ="""
<!DOCTYPE html>
<head>
<img src="cid:0"height="50" />
</head>
<body>
<div>
<h1>Warning CDD Integration Down</h1>
<h2>%s
<a href = 'https://mazetx.onschrodinger.com/livedesign/cdd_last_sync'>
Click Here For More CDD Data Sync Details
</a></h2></div>
</body>
"""%(text)
    return EMAIL_BODY

