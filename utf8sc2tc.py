import sys
import os
import ConfigParser
import traceback

resource_file = 'convert2utf8.res';
config = None
tc = ""
sc = ""

def convert_simplified_to_traditional(t_str, s_str, o_str):
    str = u""
    for i in range(0, len(o_str)) :
        if s_str.find(o_str[i]) != -1 :
            str += t_str[s_str.index(o_str[i])]
        else :
            str += o_str[i]
    return str
	

def get_mapping(cfg):
	if not cfg:
		res = os.path.join(os.path.dirname(os.path.realpath(__file__)),resource_file)
		if not os.path.isfile (res): raise "MSG_RESOURCE_FILE_NOT_FOUND"
		cfg = ConfigParser.ConfigParser()
		cfg.readfp(open(res))
		tc = cfg.get("mapping","traditional_str")
		sc = cfg.get("mapping","simplified_str")
		tc = tc.decode('utf8')
		sc = sc.decode('utf8')
	return tc, sc
	

def utf8_sc2tc(utf8_sc):
	#print os.path.dirname(os.path.realpath(__file__))
	tcmapping, scmapping = get_mapping(config)
	return convert_simplified_to_traditional(tcmapping ,scmapping, utf8_sc).encode('utf8')


def main():
	argc = len(sys.argv)

	if argc > 3 or argc == 1:
		print("MSG_WRONG_ARGC");
	elif argc == 3 :
		mode = sys.argv[2]
	elif argc == 2 :
		mode = 'gbk'
	else:
		print("MSG_WRONG_ARGC")
	
	target_file = sys.argv[1]
	
	txt = open(target_file, 'r').read()

	try:
		utf8_tc=utf8_sc2tc(txt.decode(mode))
		utf_tc = target_file+".tc"
		open(utf_tc, 'w').write(utf8_tc)
	except:
		traceback.print_exc()
		print("MSG_NOT_SUPPORT_ENCODING")


if __name__ == '__main__':
	main()

	