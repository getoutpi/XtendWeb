#!/usr/bin/python
import os
import socket
import yaml
import cgi
import cgitb


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
profile_config_file = installation_path+"/conf/profiles.yaml"


cgitb.enable()


def close_cpanel_liveapisock():
    """We close the cpanel LiveAPI socket here as we dont need those"""
    cp_socket = os.environ["CPANEL_CONNECT_SOCKET"]
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(cp_socket)
    sock.sendall('<cpanelxml shutdown="1" />')
    sock.close()


close_cpanel_liveapisock()
form = cgi.FieldStorage()


print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('<title>nDeploy</title>')
print('</head>')
print('<body>')
print('<a href="ndeploy.live.cgi"><img border="0" src="nDeploy.png" alt="nDeploy"></a>')
print('<HR>')
if form.getvalue('domain'):
    mydomain = form.getvalue('domain')
    profileyaml = installation_path + "/domain-data/" + mydomain
    if os.path.isfile(profileyaml):
        profileyaml_data_stream = open(profileyaml, 'r')
        yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        profileyaml_data_stream.close()
        customconf = yaml_parsed_profileyaml.get('customconf')
        backend_category = yaml_parsed_profileyaml.get('backend_category')
        backend_version = yaml_parsed_profileyaml.get('backend_version')
        pagespeed_status = yaml_parsed_profileyaml.get('pagespeed')
        naxsi_status = yaml_parsed_profileyaml.get('naxsi')
        profile = str(yaml_parsed_profileyaml.get('profile'))
        if os.path.isfile(profile_config_file):
            profile_data_yaml = open(profile_config_file,'r')
            profile_data_yaml_parsed = yaml.safe_load(profile_data_yaml)
            profile_data_yaml.close()
            profile_description_dict = profile_data_yaml_parsed.get(backend_category)
            profile_description = profile_description_dict.get(profile)
        else:
            print('ERROR : profile data file error')
        myhome = os.environ["HOME"]
        print(('<p style="background-color:LightGrey">CONFIGURE:  '+mydomain+'</p>'))
        print('<HR>')
        if customconf == "1":
            print('<form action="manualconfig.live.cgi" method="post">')
            print(('<p style="background-color:LightGrey">There are some MANUAL changes in the AUTO template for:  '+mydomain+'</p>'))
            print('<p style="background-color:LightGrey">Select EDIT to edit current config or RESET to reset the config to its last AUTO configured state</p>')
            print(('<p style="background-color:LightGrey">(!) All custom edits are saved in ' + myhome + '/' + mydomain + '_nginx.include.custom.conf'+'</p>'))
            print('<p style="background-color:LightGrey">Last used AUTO configured state:</p>')

            print('<div class="boxed">')
            if backend_category == "PROXY":
              print(('<p style="background-color:LightGrey">NGINX is proxying to '+backend_version+'</p>'))
            else:
              print(('<p style="background-color:LightGrey">NGINX is directly serving content using '+backend_category+'as application server(version: '+backend_version') </p>'))
            print(('<p style="background-color:LightGrey">Config template : '+profile_description+'</p>'))
            if pagespeed_status == "1":
              print('<p style="background-color:LightGrey">Google pagespeed is ACTIVE</p>')
            else:
              print('<p style="background-color:LightGrey">Google pagespeed is not enabled</p>')
            if naxsi_status == "1":
              print('<p style="background-color:LightGrey">NAXSI is in enforce mode</p>')
            else:
              print('<p style="background-color:LightGrey">NAXSI is in learning mode</p>')
            print('</div>')
            print('.boxed {border: 1px solid black ;}')
            print('<HR>')
            print('<input type="radio" name="custom" value="1" checked/> EDIT')
            print('<input type="radio" name="custom" value="0" /> RESET')
            print(('<input style="display:none" name="domain" value="'+mydomain+'">'))
            print('<input type="submit" value="Submit">')
            print('</form>')
        elif customconf == "0":
            print('<form action="autoconfig.live.cgi" method="post">')
            print('<p style="background-color:LightGrey">Current AUTO configuration:</p>')
            print('<div class="boxed">')
            if backend_category == "PROXY":
              print(('<p style="background-color:LightGrey">NGINX is proxying to '+backend_version+'</p>'))
            else:
              print(('<p style="background-color:LightGrey">NGINX is directly serving content using '+backend_category+' as application server(version: '+backend_version+') </p>'))
            print(('<p style="background-color:LightGrey">Config template : '+profile_description+'</p>'))
            if pagespeed_status == "1":
              print('<p style="background-color:LightGrey">Google pagespeed is ACTIVE</p>')
            else:
              print('<p style="background-color:LightGrey">Google pagespeed is not enabled</p>')
            if naxsi_status == "1":
              print('<p style="background-color:LightGrey">NAXSI is in enforce mode</p>')
            else:
              print('<p style="background-color:LightGrey">NAXSI is in learning mode</p>')
            print('</div>')
            print('.boxed {border: 1px solid black ;}')
            print('<HR>')
            print('<p style="background-color:LightGrey">Select AUTO to select a configuration suitable for your application</p>')
            print('<p style="background-color:LightGrey">Select MANUAL to make small changes to an AUTO configuration</p>')
            print('<HR>')
            print('<input type="radio" name="custom" value="0" checked/> AUTO')
            print('<input type="radio" name="custom" value="1" /> MANUAL')
            print(('<input style="display:none" name="domain" value="'+mydomain+'">'))
            print('<input type="submit" value="Submit">')
            print('</form>')
        else:
            print('ERROR : customconf status error in domain-data')
    else:
        print('ERROR : domain-data file i/o error')
else:
    print('ERROR : Forbidden')
print('</body>')
print('</html>')
