def wrecker(url):
    import subprocess
    output = str(subprocess.check_output("wrk -t1 -c10 -d1s http://"+url+"/productpage | grep -E 'Requests|Transfer|requests|responses'", universal_newlines=True,shell=True)).rstrip()
    return output
