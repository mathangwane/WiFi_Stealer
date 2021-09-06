#############################################
# Copyright of Sandile Mathangwane, 2021	#
# https://www.facebook.com/smathangwane		#
# https://www.github.com/mathangwane		#
#############################################

# Subprocess is used for system commands inside Python.
import subprocess

# We are going to use regular expressions.
import re


command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()

# Let's find all the wifi names which are listed after 
# "ALL User Profile     :"
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

# An empty list to save dictionaries containing all the 
# WiFi SSIDs and passwords.
wifi_list = []


# Checking for WiFi connection. If no profile name, then
# no WiFi connection.
if len(profile_names) != 0:
	for name in profile_names:
		# Create a dictionary for EACH WiFi connection
		wifi_profile = {}

		# Checking for more info on each profile. Any key?
		profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()

		# Using regex to eliminate case where no password exists.
		if re.search("Security key           : Absent", profile_info):
			continue
		else:
			# Add the SSID of the WiFi profile to the dict.
			wifi_profile["SSID"] = name

			# NOW, we can run the "key=clear" to reveal the 
			# passwords on the remaining profiles.
			profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()

			# Regex again to catch the password.
			password = re.search("Key Content            : (.*)\r", profile_info_pass)

			# Some connections have no password. We check if we
			# have found a password.
			if password == None:
				wifi_profile["PASSWORD"] = None

			else:
				# Add to password key in the dictionary.
				wifi_profile["PASSWORD"] = password[1]

			# Let's append all the WiFi info to the wifi_list var.
			wifi_list.append(wifi_profile)

for x in range(len(wifi_list)):
	print(wifi_list[x])