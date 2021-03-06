#!/usr/bin/env python


import os
import cgitb
import subprocess
import yaml
import psutil
import platform
import socket
try:
    import simplejson as json
except ImportError:
    import json


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"

cgitb.enable()


def branding_print_logo_name():
    "Branding support"
    if os.path.isfile(installation_path+"/conf/branding.yaml"):
        with open(installation_path+"/conf/branding.yaml", 'r') as brand_data_file:
            yaml_parsed_brand = yaml.safe_load(brand_data_file)
        brand_logo = yaml_parsed_brand.get("brand_logo", "xtendweb.png")
    else:
        brand_logo = "xtendweb.png"
    return brand_logo


def branding_print_banner():
    "Branding support"
    if os.path.isfile(installation_path+"/conf/branding.yaml"):
        with open(installation_path+"/conf/branding.yaml", 'r') as brand_data_file:
            yaml_parsed_brand = yaml.safe_load(brand_data_file)
        brand_name = yaml_parsed_brand.get("brand", "XtendWeb")
    else:
        brand_name = "XtendWeb"
    return brand_name


def branding_print_footer():
    "Branding support"
    if os.path.isfile(installation_path+"/conf/branding.yaml"):
        with open(installation_path+"/conf/branding.yaml", 'r') as brand_data_file:
            yaml_parsed_brand = yaml.safe_load(brand_data_file)
        brand_footer = yaml_parsed_brand.get("brand_footer", '<a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">A U T O M 8 N</a>')
    else:
        brand_footer = '<a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">A U T O M 8 N</a>'
    return brand_footer


def print_green(theoption, hint):
    print(('<div class="col-sm-6"><div class="label label-info" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'))


def print_red(theoption, hint):
    print(('<div class="col-sm-6"><div class="label label-default" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div></div>'))


print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')

print('<title>')
print(branding_print_banner())
print('</title>')

print(('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">'))
print(('<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js" crossorigin="anonymous"></script>'))
print(('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>'))
print(('<script src="js.js"></script>'))
print(('<link rel="stylesheet" href="styles.css">'))
print('</head>')
print('<body>')
print('<div id="main-container" class="container text-center">')  # marker1
print('<div class="row">')  # marker2
print('<div class="col-md-6 col-md-offset-3">')  # marker3

print('<div class="logo">')
print('<a href="xtendweb.cgi"><img border="0" src="')
print(branding_print_logo_name())
print('" width="48" height="48"></a>')
print('<h4>')
print(branding_print_banner())
print('</h4>')
print('</div>')

print('<ol class="breadcrumb">')
print('<li><a href="xtendweb.cgi"><span class="glyphicon glyphicon-repeat"></span></a></li>')
print('<li class="active">Server Config</li>')
print('</ol>')

# Next section start here
print('<div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">')  # accordion
print('<div class="panel panel-default">')  # default
print('<div class="panel-heading" role="tab" id="headingOne"><h3 class="panel-title"><a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseOne" aria-expanded="true" aria-controls="collapseOne">System Status</a></h3></div>')  # heading
print('<div id="collapseOne" class="panel-collapse collapse in" role="tabpanel" aria-labelledby="headingOne">')  # collapse
print('<div class="panel-body">')  # body
print('<div id="config">')
print('<ul class="list-group">')
print('<li class="list-group-item">')
print('<div class="row">')
nginx_status = False
for myprocess in psutil.process_iter():
    # Workaround for Python 2.6
    if platform.python_version().startswith('2.6'):
        mycmdline = myprocess.cmdline
    else:
        mycmdline = myprocess.cmdline()
    if 'nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf' in mycmdline:
        nginx_status = True
        break
if nginx_status:
    print(('<div class="col-sm-6"><div class="label label-info">ACTIVE</div></div>'))
    print(('<div class="col-sm-6 col-radio">NGINX</div>'))
else:
    print(('<div class="col-sm-6"><div class="label label-danger">INACTIVE</div></div>'))
    print(('<div class="col-sm-6 col-radio">NGINX</div>'))
print('</div>')
print('</li>')
print('<li class="list-group-item">')
print('<div class="row">')
watcher_status = False
for myprocess in psutil.process_iter():
    # Workaround for Python 2.6
    if platform.python_version().startswith('2.6'):
        mycmdline = myprocess.cmdline
    else:
        mycmdline = myprocess.cmdline()
    if '/opt/nDeploy/scripts/watcher.py' in mycmdline:
        watcher_status = True
        break
if watcher_status:
    print(('<div class="col-sm-6"><div class="label label-info">ACTIVE</div></div>'))
    print(('<div class="col-sm-6 col-radio">NDEPLOY_WATCHER</div>'))
else:
    print(('<div class="col-sm-6"><div class="label label-danger">INACTIVE</div></div>'))
    print(('<div class="col-sm-6 col-radio">NDEPLOY_WATCHER</div>'))
print('</div>')
print('</li>')
print('</ul>')
print('</div>')
print(('<div class="alert alert-info alert-top alert-btm">'))
print(('<span class="glyphicon glyphicon-circle-arrow-right" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/process_control.html">PROCESS CONTROL</a>'))
print(('</div>'))
print('</div>')  # body
print('</div>')  # collapse
print('</div>')  # default
# Next section start here
if os.path.isfile(cluster_config_file):
    print('<div class="panel panel-default">')  # default
    print('<div class="panel-heading" role="tab" id="headingTwo"><h3 class="panel-title"><a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">Cluster Status</a></h3></div>')  # heading
    print('<div id="collapseTwo" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingTwo">')  # collapse
    print('<div class="panel-body">')  # body
    print('<div id="config">')
    with open(cluster_config_file, 'r') as cluster_data_yaml:
        cluster_data_yaml_parsed = yaml.safe_load(cluster_data_yaml)
    print('<ul class="list-group">')
    for servername in cluster_data_yaml_parsed.keys():
        print('<li class="list-group-item">')
        print('<div class="row">')
        filesync_status = False
        for myprocess in psutil.process_iter():
            # Workaround for Python 2.6
            if platform.python_version().startswith('2.6'):
                mycmdline = myprocess.cmdline
            else:
                mycmdline = myprocess.cmdline()
            if '/usr/bin/unison' in mycmdline and servername in mycmdline:
                filesync_status = True
                break
        if filesync_status:
            print(('<div class="col-sm-6"><div class="label label-info">IN SYNC</div></div>'))
            print(('<div class="col-sm-6 col-radio">'+servername+'</div>'))
        else:
            print(('<div class="col-sm-6"><div class="label label-danger">OUT OF SYNC</div></div>'))
            print(('<div class="col-sm-6 col-radio">'+servername+'</div>'))
        print('</div>')
        print('</li>')
    print('</ul>')
    print('<form class="form-inline" action="fix_unison.cgi" method="post">')
    print(('<input style="display:none" name="mode" value="restart">'))
    print('<input class="btn btn-primary" type="submit" value="SOFT RESTART UNISON SYNC">')
    print('</form>')
    print(('<br>'))
    print('<form class="form-inline" action="fix_unison.cgi" method="post">')
    print(('<input style="display:none" name="mode" value="reset">'))
    print('<input class="btn btn-primary" type="submit" value="HARD RESET UNISON SYNC">')
    print('</form>')
    print(('<div class="alert alert-info alert-top">'))
    print(('Only perform a hard reset if the unison archive is corrupt.Unison archive rebuild is time consuming'))
    print(('</div>'))
    print(('</div>'))
    print('</div>')  # body
    print('</div>')  # collapse
    print('</div>')  # default
# Next section start here
# Workaround for Python 2.6
if platform.python_version().startswith('2.6'):
    listpkgs = subprocess.Popen('/usr/local/cpanel/bin/whmapi0 listpkgs --output=json', stdout=subprocess.PIPE, shell=True).communicate()[0]
else:
    listpkgs = subprocess.check_output('/usr/local/cpanel/bin/whmapi0 listpkgs --output=json', shell=True)
mypkgs = json.loads(listpkgs)
print('<div class="panel panel-default">')  # default
print('<div class="panel-heading" role="tab" id="headingThree"><h3 class="panel-title"><a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseThree" aria-expanded="false" aria-controls="collapseThree">Map cPanel pkg to nginx setting</a></h3></div>')  # heading
print('<div id="collapseThree" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingThree">')  # collapse
print('<div class="panel-body">')  # body
print('<form class="form-inline" action="pkg_profile.cgi" method="post">')
print('<select name="cpanelpkg">')
for thepkg in sorted(mypkgs.get('package')):
    pkgname = thepkg.get('name').encode('utf-8').replace(' ', '_')
    print(('<option value="'+pkgname+'">'+pkgname+'</option>'))
print('</select>')
print('<input class="btn btn-primary" type="submit" value="EDIT PKG">')
print('</form>')
print(('<div class="alert alert-info alert-top">'))
print(('If you enable config change with package, nginx config for domain will be reset to package setting on plan upgrade/downgrade and all user settings will be lost'))
print(('</div>'))
if os.path.isfile(installation_path+'/conf/lock_domaindata_to_package'):
    print('<form class="form-group" action="lock_domain_data_to_package.cgi">')
    print('<input class="btn btn-primary" type="submit" value="DISABLE CONFIG CHANGE WITH PKG">')
    print(('<input class="hidden" name="package_lock" value="disabled">'))
    print('</form>')
else:
    print('<form class="form-group" action="lock_domain_data_to_package.cgi">')
    print('<input class="btn btn-warning" type="submit" value="ENABLE CONFIG CHANGE WITH PKG">')
    print(('<input class="hidden" name="package_lock" value="enabled">'))
    print('</form>')
print('</div>')  # body
print('</div>')  # collapse
print('</div>')  # default

# Next section start here
print('<div class="panel panel-default">')  # default
print('<div class="panel-heading" role="tab" id="headingFour"><h3 class="panel-title"><a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseFour" aria-expanded="false" aria-controls="collapseFour">PHP-FPM Pool Editor</a></h3></div>')  # heading
print('<div id="collapseFour" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingFour">')  # collapse
print('<div class="panel-body">')  # body
print('<form class="form-inline" action="phpfpm_pool_editor.cgi" method="post">')
print('<select name="poolfile">')
if os.path.isfile(installation_path+"/conf/secure-php-enabled"):
    conf_list = os.listdir("/opt/nDeploy/secure-php-fpm.d")
    for filename in sorted(conf_list):
        user, extension = filename.split('.')
        if user != 'nobody':
            print(('<option value="/opt/nDeploy/secure-php-fpm.d/'+filename+'">'+user+'</option>'))
else:
    conf_list = os.listdir("/opt/nDeploy/php-fpm.d")
    for filename in sorted(conf_list):
        user, extension = filename.split('.')
        if user != 'nobody':
            print(('<option value="/opt/nDeploy/php-fpm.d/'+filename+'">'+user+'</option>'))
print('</select>')
if os.path.isfile(installation_path+"/conf/secure-php-enabled"):
    print(('<input class="hidden" name="section" value="1">'))
else:
    print(('<input class="hidden" name="section" value="0">'))
print('<input class="btn btn-primary" type="submit" value="EDIT PHP SETTINGS">')
print('</form>')
print('</div>')  # body
print('</div>')  # collapse
print('</div>')  # default

# Next section start here
with open('/etc/redhat-release', 'r') as releasefile:
    osrelease = releasefile.read().split(' ')[0]
if not osrelease == 'CloudLinux':
    if os.path.isfile('/usr/bin/systemctl'):
        # Next sub-section start here
        if os.path.isfile(installation_path+"/conf/secure-php-enabled"):  # if per user php-fpm master process is set
            userlist = os.listdir("/var/cpanel/users")
            print('<div class="panel panel-default">')  # default
            print('<div class="panel-heading" role="tab" id="headingFive"><h3 class="panel-title"><a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseFive" aria-expanded="false" aria-controls="collapseFive">Resource Limit</a></h3></div>')  # heading
            print('<div id="collapseFive" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingFive">')  # collapse
            print('<div class="panel-body">')  # body
            print('<div class="row">')  # markerr1
            print('<div class="col-sm-6">')  # markerc1
            print('<div class="panel panel-default">')  # markerp1
            print('<div class="panel-heading"><h3 class="panel-title">User</h3></div>')
            print('<div class="panel-body">')  # markerb1
            print('<form class="form-inline" action="resource_limit.cgi" method="post">')
            print('<select name="unit">')
            for cpuser in sorted(userlist):
                if cpuser != 'nobody' and cpuser != 'system':
                    print(('<option value="'+cpuser+'">'+cpuser+'</option>'))
            print('</select>')
            print(('<input style="display:none" name="mode" value="user">'))
            print(('<br>'))
            print(('<br>'))
            print('<input class="btn btn-primary" type="submit" value="SET LIMIT">')
            print('</form>')
            print('</div>')  # markerb1
            print('</div>')  # markerp1
            print('</div>')  # markerc1
            print('<div class="col-sm-6">')  # markerc2
            print('<div class="panel panel-default">')  # markerp2
            print('<div class="panel-heading"><h3 class="panel-title">Service</h3></div>')
            print('<div class="panel-body">')  # markerb2
            print('<form class="form-inline" action="resource_limit.cgi" method="post">')
            print('<select name="unit">')
            for service in "nginx", "httpd", "mysql", "ndeploy_backends", "ea-php54-php-fpm", "ea-php55-php-fpm", "ea-php56-php-fpm", "ea-php70-php-fpm", "ea-php71-php-fpm", "ea-php72-php-fpm":
                print(('<option value="'+service+'">'+service+'</option>'))
            print('</select>')
            print(('<input style="display:none" name="mode" value="service">'))
            print(('<br>'))
            print(('<br>'))
            print('<input class="btn btn-primary" type="submit" value="SET LIMIT">')
            print('</form>')
            print('</div>')  # markerb2
            print('</div>')  # markerp2
            print('</div>')  # markerc2
            print('</div>')  # markerr1
            print('</div>')  # body
            print('</div>')  # collapse
            print('</div>')  # default
        else:
            # Next sub-section start here
            print('<div class="panel panel-default">')  # default
            print('<div class="panel-heading" role="tab" id="headingFive"><h3 class="panel-title"><a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseFive" aria-expanded="false" aria-controls="collapseFive">Resource Limit</a></h3></div>')  # heading
            print('<div id="collapseFive" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingFive">')  # collapse
            print('<div class="panel-body">')  # body
            print(('<div class="alert alert-info">'))
            print(('BlockIOWeight range is 10-1000, CPUShares range is 0-1024, MemoryLimit range is calculated using available memory'))
            print(('</div>'))
            print('<form class="form-inline" action="resource_limit.cgi" method="post">')
            print('<select name="unit">')
            for service in "nginx", "httpd", "mysql", "ndeploy_backends", "ea-php54-php-fpm", "ea-php55-php-fpm", "ea-php56-php-fpm", "ea-php70-php-fpm", "ea-php71-php-fpm", "ea-php72-php-fpm":
                print(('<option value="'+service+'">'+service+'</option>'))
            print('</select>')
            print(('<input style="display:none" name="mode" value="service">'))
            print('<input class="btn btn-primary" type="submit" value="SET LIMIT">')
            print('</form>')
            print('</div>')  # body
            print('</div>')  # collapse
            print('</div>')  # default
# Next section start here
print('<div class="panel panel-default">')  # default
print('<div class="panel-heading" role="tab" id="headingSeven"><h3 class="panel-title"><a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseSeven" aria-expanded="false" aria-controls="collapseSeven">Set Default PHP for AutoConfig</a></h3></div>')  # heading
print('<div id="collapseSeven" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingSeven">')  # collapse
print('<div class="panel-body">')  # body
if os.path.isfile(installation_path+"/conf/preferred_php.yaml"):
    preferred_php_yaml = open(installation_path+"/conf/preferred_php.yaml", 'r')
    preferred_php_yaml_parsed = yaml.safe_load(preferred_php_yaml)
    preferred_php_yaml.close()
    phpversion = preferred_php_yaml_parsed.get('PHP')
    print('<div class="alert alert-success">')
    print(('Current default PHP: <span class="label label-success">'+phpversion.keys()[0])+'</span>')
    print('</div>')
    print('<div class="alert alert-info">')
    print('If MultiPHP is enabled, the PHP version selected by MultiPHP is used by autoconfig. It is recommended that MultiPHP is enabled for all accounts for best results')
    print('</div>')
print('<form class="form-inline" action="set_default_php.cgi" method="post">')
print('<select name="phpversion">')
backend_config_file = installation_path+"/conf/backends.yaml"
backend_data_yaml = open(backend_config_file, 'r')
backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
backend_data_yaml.close()
if "PHP" in backend_data_yaml_parsed:
    php_backends_dict = backend_data_yaml_parsed["PHP"]
    for versions_defined in list(php_backends_dict.keys()):
        print(('<option value="'+versions_defined+'">'+versions_defined+'</option>'))
print('</select>')
print('<input class="btn btn-primary" type="submit" value="SET DEFAULT PHP">')
print('</form>')
print('</div>')  # body
print('</div>')  # collapse
print('</div>')  # default
# Next section start here
if os.path.isfile(cluster_config_file):
    print('<div class="panel panel-default">')  # default
    print('<div class="panel-heading" role="tab" id="headingEight"><h3 class="panel-title"><a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseEight" aria-expanded="false" aria-controls="collapseEight">Sync GeoDNS zone</a></h3></div>')  # heading
    print('<div id="collapseEight" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingEight">')  # collapse
    print('<div class="panel-body">')  # body
    print('<form class="form-inline" action="sync_gdnsd_zone.cgi" method="post">')
    print('<select name="user">')
    user_list = os.listdir("/var/cpanel/users")
    for cpuser in sorted(user_list):
        if cpuser != 'nobody' and cpuser != 'system':
            print(('<option value="'+cpuser+'">'+cpuser+'</option>'))
    print('</select>')
    print(('<br>'))
    print(('<br>'))
    print('<input class="btn btn-primary" type="submit" value="SYNC DNS ZONE">')
    print('</form>')
    print('</div>')  # body
    print('</div>')  # collapse
    print('</div>')  # default
# Next section start here
print('<div class="panel panel-default">')  # default
print('<div class="panel-heading" role="tab" id="headingNine"><h3 class="panel-title"><a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseNine" aria-expanded="false" aria-controls="collapseNine">ABNORMAL PROCESS TRACKER</a></h3></div>')  # heading
print('<div id="collapseNine" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingNine">')  # collapse
print('<div class="panel-body">')  # body
print('<form class="form-group" action="abnormal_process_detector.cgi">')
print('<input class="btn btn-primary" type="submit" value="CHECK PROCESS">')
print('</form>')
print('</div>')  # body
print('</div>')  # collapse
print('</div>')  # default
# Next section start here
print('<div class="panel panel-default">')  # default
print('<div class="panel-heading" role="tab" id="headingTen"><h3 class="panel-title"><a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseTen" aria-expanded="false" aria-controls="collapseTen">NETDATA</a></h3></div>')  # heading
print('<div id="collapseTen" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingTen">')  # collapse
myhostname = socket.gethostname()
print('<div class="panel-body">')  # body
print('<form class="form-group" action="https://'+myhostname+'/netdata/" target="_blank">')
print('<input class="btn btn-primary" type="submit" value="NETDATA">')
print('</form>')
print('</div>')  # body
print('</div>')  # collapse
print('</div>')  # default
print('</div>')  # accordion

print('<div class="panel-footer"><small>')
print(branding_print_footer())
print('</small></div>')

print('</div>')  # marker3
print('</div>')  # marker2
print('</div>')  # marker1
print('</body>')
print('</html>')
