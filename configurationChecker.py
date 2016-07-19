import ConfigParser

def check_cinder_api(api):
	cinder_barbican_api = "cinder.keymgr.barbican.BarbicanKeyManager"
	if (api == cinder_barbican_api):
		return True
	return False

def check_nova_api(api):
        nova_barbican_api = "nova.keymgr.barbican.BarbicanKeyManager"
        if (api == nova_barbican_api):
                return True
        return False

def MyParser(configFile):
	config = ConfigParser.ConfigParser()
	config.read(configFile)
	if not config.has_section("keymgr"): 
		print ("ERROR: %s Non ha la sezione keymgr" % configFile)
	elif config.has_option("keymgr","fixed_key"):
		print ("ERROR: Fixed key in %s" % configFile)
	elif not config.has_option("keymgr","api_class"):
 		print ("ERROR: %s Non ha la sezione api_class" % configFile)
	else:
		return config.get("keymgr","api_class")

def retrieve_nova_configuration():
	nova_config_file="/etc/nova/nova.conf"
        assert nova_config_file is not None
        return MyParser(nova_config_file)

def retrieve_cinder_configuration():
        cinder_config_file="/etc/cinder/cinder.conf"
        assert cinder_config_file is not None
        return MyParser(cinder_config_file)

def retrieve_services_configurations():
        return retrieve_nova_configuration(), retrieve_cinder_configuration()



def check_api():
	nova, cinder =  retrieve_services_configurations()
	return check_cinder_api(cinder), check_nova_api(nova)

#enabled_crypto_plugins = simple_crypto
#def MyBarbicanParser(configFile):
#        config = ConfigParser.ConfigParser()
#        config.read(configFile)
#	if not config.has_section("secretstore"):
#		print ("ERROR: %s Non ha la sezione secretstore" % configFile)
#        elif not config.has_section("crypto"):
#                print ("ERROR: %s Non ha la sezione crypto" % configFile)
#        elif not config.has_option("crypto","enabled_crypto_plugins"):
#		print ("ERROR: %s Non ha la sezione enabled_crypto_plugins" % configFile)
#        else:
#                return config.get("crypto","enabled_crypto_plugins")
def esp_check(config):
#	if not (config.has_section("pk11_crypto_plugin")) or (if not (config.has_section("crypto"))):
#		return False
	if config.has_section("pk11_crypto_plugin"):
		return True
	if config.has_section("crypto"):
		if not config.has_option("crypto","enabled_crypto_plugins"):
			return False
		elif (config.get("crypto","enabled_crypto_plugins") == "simple_crypto"):
			print("NOT SAFE!")
			return False
	return False



def plugin_check(config):
	esp = config.get("secretstore","enabled_secretstore_plugins")
	if (esp == "store_crypto"):
		return esp_check(config)
	elif (esp == "kmip_crypto"):
		if not config.has_section("kmip_plugin"):
			return False
		else:
			return True
	return False



def MyBarbicanParser(configFile):
        config = ConfigParser.ConfigParser()
        config.read(configFile)
        if not config.has_section("secretstore"):
                print ("ERROR: %s Non ha la sezione secretstore" % configFile)
		return False
        elif not config.has_option("secretstore","enabled_secretstore_plugins"):
		return False
	else:
		return plugin_check(config) 


#	elif not config.has_section("crypto"):
 #               print ("ERROR: %s Non ha la sezione crypto" % configFile)
  #      elif not config.has_option("crypto","enabled_crypto_plugins"):
   #             print ("ERROR: %s Non ha la sezione enabled_crypto_plugins" % configFile)
    #    else:
     #           return config.get("crypto","enabled_crypto_plugins")



def check_barbican_conf():
	barbican_conf_file = "/etc/barbican/barbican.conf"
	barbican = MyBarbicanParser(barbican_conf_file)
	print (barbican)
	if (barbican == False):
		print ("WARNING: Barbican plugin not safe for production deployment")
		return False
	return True

print check_api()
check_barbican_conf()



