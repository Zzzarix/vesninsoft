import xml.etree.ElementTree as et

f = et.parse(r"D:\Downloads\РасчетныеЛистки_202211_7708154628.xml")
print(f.getroot().attrib)
