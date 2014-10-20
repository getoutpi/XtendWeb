#!/usr/bin/env python

import yaml
import argparse
import os

installation_path = "/opt/xstack" #Absolute Installation Path

#Function defs
def nginx_confgen_profilegen(domain_name,user_name,cpanelip,sslenabled):
	"Function generating config include based on profile"
	profileyaml = installation_path+"/domain-data/"+domain_name
	if os.path.isfile(profileyaml):
		if sslenabled = 1:
			include_file = "/etc/nginx/sites-enabled/"+domain_name+"_ssl.include"
		else:
			include_file = "/etc/nginx/sites-enabled/"+domain_name+".include"
		profileyaml_data_stream = open(profileyaml,'r')
		yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
		profile_custom_status = yaml_parsed_profileyaml.get('customconf')
		if profile_custom_status == 0:
			profile_category = yaml_parsed_profileyaml.get('backend_category')
			profile_code = yaml_parsed_profileyaml.get('profile') 
			if profile_category == "PHP":
				#Code to deal with php-fpm 
			else:
				profile_template_file = open(installation_path+"/conf/"+profile_code+".tmpl",'r')
				profile_config_out = open(include_file,'w')
				for line in profile_template_file:
					line = line.replace('CPANELIP',cpanelip)
					config_out.write(line)
				profile_template_file.close()
				profile_config_out.close()
		elif profile_custom_status == 1:
			#Code to validate nginx custom conf goes here
		else:
			return
	else:
		template_file = open(installation_path+"/conf/domain_data.yaml.tmpl",'r')
		config_out = open(installation_path+"/domain-data/"+domain_name,'w')
		for line in template_file:
			line = line.replace('CPANELUSER',user_name)
			config_out.write(line)
		template_file.close()
		config_out.close()
		nginx_confgen_profilegen(domain_name,user_name,cpanelip,sslenabled)


def nginx_confgen(user_name,domain_name):
	"Function that generates nginx config given a domain name"
	cpdomainyaml = "/var/cpanel/userdata/"+user_name+"/"+domain_name
	cpaneldomain_data_stream = open(cpdomainyaml,'r')
	yaml_parsed_cpaneldomain = yaml.safe_load(cpaneldomain_data_stream)
	cpanel_ipv4 = yaml_parsed_cpaneldomain.get('ip')
	domain_sname = yaml_parsed_cpaneldomain.get('servername')
	domain_aname = yaml_parsed_cpaneldomain.get('serveralias')
	domain_list = domain_sname+" "+domain_aname
	if 'ipv6' in yaml_parsed_cpaneldomain.keys():
		for ipv6_addr in yaml_parsed_cpaneldomain.get('ipv6').keys():
			cpanel_ipv6 = "listen ["+ipv6_addr+"]"
	else:
		cpanel_ipv6 = "#CPIPVSIX"
	if 'ssl' in yaml_parsed_cpaneldomain.keys():
		cpdomainyaml_ssl = "/var/cpanel/userdata/"+user_name+"/"+domain_name+"_SSL"
		cpaneldomain_ssl_data_stream = open(cpdomainyaml_ssl,'r')
		yaml_parsed_cpaneldomain_ssl = yaml.safe_load(cpaneldomain_ssl_data_stream)
		sslcertificatefile = yaml_parsed_cpaneldomain_ssl.get('sslcertificatefile')
		sslcertificatekeyfile = yaml_parsed_cpaneldomain_ssl.get('sslcertificatekeyfile')
		sslcacertificatefile = yaml_parsed_cpaneldomain_ssl.get('sslcacertificatefile') 
		sslcombinedcert = "/etc/nginx/ssl/"+domain_name+".crt"
		os.system("cat /dev/null > "+sslcombinedcert)
		if sslcacertificatefile:
			os.system("cat "+sslcertificatefile+" "+sslcacertificatefile+" >> "+sslcombinedcert)
		else:
			os.system("cat "+sslcertificatefile+" >> "+sslcombinedcert)
		template_file = open(installation_path+"/conf/server_ssl.tmpl",'r')
		config_out = open("/etc/nginx/sites-enabled/"+domain_name+"_SSL.conf",'w')
		for line in template_file:
			line = line.replace('CPANELIP',cpanel_ipv4)
			line = line.replace('DOMAINLIST',domain_list)
			line = line.replace('DOMAINNAME',domain_sname)
			line = line.replace('#CPIPVSIX',cpanel_ipv6)
			line = line.replace('CPANELSSLKEY',sslcertificatekeyfile)
			line = line.replace('CPANELSSLCRT',sslcombinedcert)
			config_out.write(line)
		template_file.close()
		config_out.close()
	else:
		template_file = open(installation_path+"/conf/server.tmpl",'r')
		config_out = open("/etc/nginx/sites-enabled/"+domain_name+".conf",'w')
		for line in template_file:
			line = line.replace('CPANELIP',cpanel_ipv4)
			line = line.replace('DOMAINNAME',domain_list)
			line = line.replace('#CPIPVSIX',cpanel_ipv6)
			config_out.write(line)
		template_file.close()
		config_out.close()



#End Function defs

parser = argparse.ArgumentParser(description = "Regenerate nginX and app server configs for cpanel user")
parser.add_argument("CPANELUSER")
args = parser.parse_args()
cpaneluser = args.CPANELUSER

cpuserdatayaml = "/var/cpanel/userdata/"+cpaneluser+"/main"
plugin_user_datayaml = installation_path+"/userdata/"+cpaneluser

cpaneluser_data_stream = open(cpuserdatayaml,'r')
yaml_parsed_cpaneluser = yaml.safe_load(cpaneluser_data_stream)

main_domain = yaml_parsed_cpaneluser.get('main_domain')   
#parked_domains = yaml_parsed_cpaneluser.get('parked_domains')   #This data is irrelevant as parked domain list is in ServerAlias
#addon_domains = yaml_parsed_cpaneluser.get('addon_domains')     #This data is irrelevant as addon is mapped to a subdomain
sub_domains = yaml_parsed_cpaneluser.get('sub_domains')

nginx_confgen(cpaneluser,main_domain) #Generate conf for main domain

for domain_in_subdomains in sub_domains:
	nginx_confgen(cpaneluser,domain_in_subdomains) #Generate conf for sub domains which takes care of addon as well
