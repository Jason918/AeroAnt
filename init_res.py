__author__ = 'admin'

res_xml_file_path = "reslist_view.xml"

from ResPool import client
print client.reset_res_pool()
print client.add_res_from_file(res_xml_file_path)